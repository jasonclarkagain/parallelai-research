#!/usr/bin/env python3
"""
ParallelAI API Server - Secure Key-Based Access
"""
import asyncio
import json
import secrets
import hashlib
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

# Fix import path - add parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    from fastapi import FastAPI, HTTPException, Depends
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install with: pip install fastapi uvicorn httpx")
    sys.exit(1)

# Now import your existing ParallelAI functionality
try:
    from src.parallelai.key_manager import load_keys
    from src.real_swarm import WorkingSwarm
    print("✅ Successfully imported ParallelAI modules")
except ImportError as e:
    print(f"❌ Failed to import ParallelAI modules: {e}")
    print("Make sure you're running from the parallelai directory")
    sys.exit(1)

# Initialize FastAPI app
app = FastAPI(
    title="ParallelAI API Server",
    description="Secure API for ParallelAI multi-LLM research platform",
    version="1.0.0"
)

# CORS middleware for web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# In-memory key storage
class APIKeyManager:
    def __init__(self, storage_file="~/.parallelai/api_keys.json"):
        self.storage_file = os.path.expanduser(storage_file)
        self.keys = self.load_keys()
    
    def load_keys(self) -> Dict[str, Dict]:
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_keys(self):
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
        with open(self.storage_file, 'w') as f:
            json.dump(self.keys, f, indent=2)
    
    def generate_key(self, name: str, scopes: List[str] = None) -> str:
        api_key = f"pai_{secrets.token_urlsafe(32)}"
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        self.keys[key_hash] = {
            "name": name,
            "scopes": scopes or ["query"],
            "created": datetime.now().isoformat(),
            "last_used": None,
            "usage_count": 0,
            "is_active": True
        }
        
        self.save_keys()
        return api_key
    
    def validate_key(self, api_key: str) -> Optional[Dict]:
        if not api_key:
            return None
        
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        if key_hash in self.keys:
            key_data = self.keys[key_hash]
            if key_data.get("is_active", True):
                key_data["last_used"] = datetime.now().isoformat()
                key_data["usage_count"] = key_data.get("usage_count", 0) + 1
                self.save_keys()
                return key_data
        
        return None
    
    def revoke_key(self, api_key: str) -> bool:
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        if key_hash in self.keys:
            self.keys[key_hash]["is_active"] = False
            self.save_keys()
            return True
        
        return False
    
    def list_keys(self) -> List[Dict]:
        result = []
        for key_hash, key_data in self.keys.items():
            result.append({
                "name": key_data.get("name", "Unnamed"),
                "scopes": key_data.get("scopes", []),
                "created": key_data.get("created"),
                "last_used": key_data.get("last_used"),
                "usage_count": key_data.get("usage_count", 0),
                "is_active": key_data.get("is_active", True),
                "id": key_hash[:8]
            })
        return result

# Initialize key manager
key_manager = APIKeyManager()

# Dependency for API key authentication
async def verify_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict:
    api_key = credentials.credentials
    key_data = key_manager.validate_key(api_key)
    
    if not key_data:
        raise HTTPException(
            status_code=401,
            detail="Invalid or inactive API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return key_data

# API Routes
@app.get("/")
async def root():
    return {
        "service": "ParallelAI API",
        "version": "1.0.0",
        "endpoints": [
            "/docs - API documentation",
            "/keys - Manage API keys",
            "/query - Query AI providers",
            "/status - Check service status",
            "/providers - List available providers"
        ]
    }

@app.get("/status")
async def get_status():
    return {
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "providers_configured": len(load_keys())
    }

@app.get("/providers")
async def list_providers():
    keys = load_keys()
    providers = []
    
    for provider, key in keys.items():
        if key:
            providers.append({
                "name": provider,
                "configured": True,
                "key_present": True
            })
        else:
            providers.append({
                "name": provider,
                "configured": False,
                "key_present": False
            })
    
    return {"providers": providers}

@app.post("/keys/generate")
async def generate_key(name: str, scopes: Optional[List[str]] = None):
    if not name:
        raise HTTPException(status_code=400, detail="Key name is required")
    
    api_key = key_manager.generate_key(name, scopes)
    
    return {
        "message": "API key generated successfully",
        "api_key": api_key,
        "warning": "Store this key securely - it won't be shown again",
        "name": name,
        "scopes": scopes or ["query"]
    }

@app.get("/keys/list")
async def list_keys():
    keys = key_manager.list_keys()
    return {"keys": keys, "total": len(keys)}

@app.post("/keys/revoke/{key_id}")
async def revoke_key(key_id: str, api_key: str):
    if key_manager.revoke_key(api_key):
        return {"message": f"Key {key_id[:8]}... revoked successfully"}
    else:
        raise HTTPException(status_code=404, detail="Key not found or invalid")

@app.post("/query")
async def query_ai(
    query: str,
    provider: Optional[str] = None,
    key_data: Dict = Depends(verify_api_key)
):
    if "query" not in key_data.get("scopes", []):
        raise HTTPException(
            status_code=403,
            detail="API key does not have query permission"
        )
    
    if not query or len(query.strip()) < 1:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    if len(query) > 5000:
        raise HTTPException(status_code=400, detail="Query too long (max 5000 chars)")
    
    try:
        async with WorkingSwarm() as swarm:
            if provider:
                result = await swarm.query_specific(provider, query)
                
                if result.get("success"):
                    return {
                        "success": True,
                        "provider": provider,
                        "model": result.get("model"),
                        "response": result["response"],
                        "usage": result.get("usage", {}),
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "provider": provider,
                        "error": result.get("error"),
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                results = await swarm.query_all(query)
                
                formatted_results = {}
                for prov, result in results.items():
                    if result.get("success"):
                        formatted_results[prov] = {
                            "success": True,
                            "model": result.get("model"),
                            "response": result["response"][:1000],
                            "usage": result.get("usage", {})
                        }
                    else:
                        formatted_results[prov] = {
                            "success": False,
                            "error": result.get("error")
                        }
                
                return {
                    "success": True,
                    "query": query,
                    "results": formatted_results,
                    "timestamp": datetime.now().isoformat(),
                    "total_providers": len(results)
                }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Query failed: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    print("🚀 Starting ParallelAI API Server...")
    print("📡 Endpoints:")
    print("   • http://localhost:8000 - API server")
    print("   • http://localhost:8000/docs - Interactive documentation")
    print("   • http://localhost:8000/keys/generate - Generate API keys")
    print("\n🔐 Security note: API keys are hashed and stored securely")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

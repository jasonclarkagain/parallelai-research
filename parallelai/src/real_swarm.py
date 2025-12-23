"""
Real Working Swarm for ParallelAI
CLEAN VERSION: No debug prints
"""
import asyncio
import aiohttp
from typing import Dict, Any
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import API_ENDPOINTS, DEFAULT_MODELS, get_headers
from src.parallelai.key_manager import load_keys

class WorkingSwarm:
    def __init__(self):
        # Load keys from key manager
        self.keys = load_keys()
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _query_api(self, provider: str, query: str) -> Dict[str, Any]:
        """Generic API query method"""
        if not self.keys.get(provider):
            return {"success": False, "error": f"{provider} API key not set"}
        
        try:
            # Prepare payload
            if provider == "anthropic":
                payload = {
                    "model": DEFAULT_MODELS[provider],
                    "max_tokens": 1000,
                    "messages": [{"role": "user", "content": query}]
                }
            else:
                payload = {
                    "model": DEFAULT_MODELS[provider],
                    "messages": [{"role": "user", "content": query}],
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
            
            headers = get_headers(provider, self.keys[provider])
            
            async with self.session.post(
                API_ENDPOINTS[provider],
                headers=headers,
                json=payload,
                timeout=30
            ) as response:
                response_text = await response.text()
                
                if response.status == 200:
                    data = await response.json()
                    
                    # Extract response based on provider format
                    if provider == "anthropic":
                        response_content = data['content'][0]['text']
                    elif provider in ["openai", "groq", "together", "openrouter"]:
                        response_content = data['choices'][0]['message']['content']
                    else:
                        response_content = str(data)
                    
                    return {
                        "success": True,
                        "response": response_content,
                        "model": data.get('model', DEFAULT_MODELS[provider]),
                        "usage": data.get('usage', {})
                    }
                else:
                    return {
                        "success": False,
                        "error": f"{provider} API error: {response.status}",
                        "details": response_text[:200]
                    }
        except Exception as e:
            return {"success": False, "error": f"{provider} request failed: {str(e)}"}
    
    async def query_all(self, query: str) -> Dict[str, Dict[str, Any]]:
        """Query all available APIs in parallel"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        # Get available providers with keys
        available_providers = [p for p in ['openai', 'anthropic', 'groq', 'together', 'openrouter'] 
                              if self.keys.get(p)]
        
        if not available_providers:
            return {"error": "No API keys configured. Run 'parallelai keys setup'"}
        
        # Create tasks
        tasks = []
        for provider in available_providers:
            tasks.append(self._query_api(provider, query))
        
        # Run in parallel
        results = {}
        completed = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(completed):
            provider = available_providers[i]
            if isinstance(result, Exception):
                results[provider] = {"success": False, "error": str(result)}
            else:
                results[provider] = result
        
        return results
    
    async def query_specific(self, provider: str, query: str) -> Dict[str, Any]:
        """Query a specific provider"""
        return await self._query_api(provider, query)

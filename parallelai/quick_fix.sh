#!/bin/bash

echo "🚀 Quick Fix for ParallelAI Imports"
echo "==================================="

# Create minimal working config
cat > src/config.py << 'CONFIG_EOF'
"""
Minimal Working Config for ParallelAI
"""
API_ENDPOINTS = {
    "openai": "https://api.openai.com/v1/chat/completions",
    "anthropic": "https://api.anthropic.com/v1/messages",
    "groq": "https://api.groq.com/openai/v1/chat/completions",
    "together": "https://api.together.xyz/v1/chat/completions",
}

DEFAULT_MODELS = {
    "openai": "gpt-3.5-turbo",
    "anthropic": "claude-3-haiku-20240307",
    "groq": "llama3-8b-8192",
    "together": "meta-llama/Llama-3-70b-chat-hf",
}

def get_headers(provider: str, api_key: str) -> dict:
    if provider == "openai":
        return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    elif provider == "anthropic":
        return {"x-api-key": api_key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"}
    elif provider == "groq":
        return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    elif provider == "together":
        return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    else:
        return {"Content-Type": "application/json"}

# For backward compatibility
API_KEYS = {}
HEADERS = {}
CONFIG_EOF

echo "✅ Created minimal config.py"
echo "✅ All required variables defined"

# Test it
python3 -c "
import sys
sys.path.insert(0, '.')
from src.config import API_ENDPOINTS, DEFAULT_MODELS, get_headers
print('✅ Import test passed!')
print(f'Endpoints: {list(API_ENDPOINTS.keys())}')
"

echo ""
echo "🎉 Now try: ./parallelai query --provider openai 'Hello'"

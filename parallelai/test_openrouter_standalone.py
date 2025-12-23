#!/usr/bin/env python3
"""
Standalone OpenRouter test
"""
import asyncio
import aiohttp
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.config import API_ENDPOINTS, DEFAULT_MODELS, get_headers

async def test_openrouter_direct():
    """Test OpenRouter directly without the swarm"""
    print("🧪 Testing OpenRouter directly...")
    
    # Read key directly from config
    config_file = Path.home() / '.parallelai' / 'config'
    import configparser
    config = configparser.ConfigParser()
    config.read(config_file)
    
    openrouter_key = config.get('api_keys', 'openrouter', fallback='')
    
    if not openrouter_key:
        print("❌ No OpenRouter key in config")
        return
    
    print(f"🔑 Key from config: {openrouter_key[:12]}... ({len(openrouter_key)} chars)")
    
    headers = get_headers('openrouter', openrouter_key)
    print(f"📋 Headers being sent: {headers.keys()}")
    
    payload = {
        "model": DEFAULT_MODELS['openrouter'],
        "messages": [{"role": "user", "content": "Hello from direct test"}],
        "temperature": 0.7,
        "max_tokens": 50
    }
    
    print(f"📦 Payload model: {payload['model']}")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                API_ENDPOINTS['openrouter'],
                headers=headers,
                json=payload,
                timeout=15
            ) as response:
                response_text = await response.text()
                print(f"📊 Status: {response.status}")
                print(f"📄 Response headers: {dict(response.headers)}")
                
                if response.status == 200:
                    import json
                    data = json.loads(response_text)
                    print(f"✅ Success! Response: {data['choices'][0]['message']['content']}")
                    return True
                else:
                    print(f"❌ Error {response.status}: {response_text[:200]}")
                    return False
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False

if __name__ == "__main__":
    asyncio.run(test_openrouter_direct())

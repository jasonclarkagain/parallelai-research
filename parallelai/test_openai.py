#!/usr/bin/env python3
import asyncio
import aiohttp
import time
from src.config import API_ENDPOINTS, DEFAULT_MODELS, get_headers
from src.parallelai.key_manager import load_keys

async def test_openai():
    keys = load_keys()
    
    if not keys.get('openai'):
        print("❌ No OpenAI API key")
        return
    
    print("🧪 Testing OpenAI with delay...")
    
    headers = get_headers('openai', keys['openai'])
    payload = {
        "model": DEFAULT_MODELS['openai'],
        "messages": [{"role": "user", "content": "Say hello"}],
        "temperature": 0.7,
        "max_tokens": 10
    }
    
    async with aiohttp.ClientSession() as session:
        # Add delay to avoid rate limits
        print("Waiting 2 seconds to avoid rate limit...")
        await asyncio.sleep(2)
        
        async with session.post(
            API_ENDPOINTS['openai'],
            headers=headers,
            json=payload,
            timeout=30
        ) as response:
            print(f"Status: {response.status}")
            if response.status == 200:
                data = await response.json()
                print(f"✅ OpenAI working! Response: {data['choices'][0]['message']['content']}")
            elif response.status == 429:
                print("❌ Rate limited. Wait a few minutes and try again.")
                print("Tip: OpenAI free tier has strict limits.")
            else:
                print(f"❌ Error: {await response.text()[:100]}")

if __name__ == "__main__":
    asyncio.run(test_openai())

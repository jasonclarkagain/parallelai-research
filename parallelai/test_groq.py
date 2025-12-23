#!/usr/bin/env python3
import asyncio
import aiohttp
from src.parallelai.key_manager import load_keys

async def test_groq_models():
    keys = load_keys()
    
    if not keys.get('groq'):
        print("❌ No Groq API key")
        return
    
    print("🔍 Checking available Groq models...")
    
    headers = {
        "Authorization": f"Bearer {keys['groq']}",
        "Content-Type": "application/json"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.groq.com/openai/v1/models",
            headers=headers,
            timeout=10
        ) as response:
            if response.status == 200:
                data = await response.json()
                print("✅ Available Groq models:")
                for model in data['data']:
                    print(f"  • {model['id']}")
            else:
                print(f"❌ Error {response.status}: {await response.text()[:100]}")

if __name__ == "__main__":
    asyncio.run(test_groq_models())

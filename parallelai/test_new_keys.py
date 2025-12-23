import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

async def test_provider(name, url, headers_func, payload_func):
    key = os.getenv(f'{name.upper()}_API_KEY') or os.getenv(f'{name.upper()}_TOKEN')
    
    if not key or 'NEW_' in key or 'GET_' in key:
        print(f"⚠️  {name}: No valid key configured")
        return False
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=payload_func(key),
                headers=headers_func(key),
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    print(f"✅ {name}: Works with new key")
                    return True
                else:
                    print(f"❌ {name}: Failed (HTTP {response.status})")
                    return False
    except Exception as e:
        print(f"❌ {name}: Error - {str(e)[:50]}")
        return False

# Test Groq
async def test_all():
    print("🔐 Testing NEW API Keys...")
    
    tests = []
    
    # Test Groq if key exists
    if os.getenv('GROQ_API_KEY') and 'NEW_' not in os.getenv('GROQ_API_KEY'):
        tests.append(test_provider(
            'groq',
            'https://api.groq.com/openai/v1/chat/completions',
            lambda key: {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
            lambda key: {'model': 'llama-3.3-70b-versatile', 'messages': [{'role': 'user', 'content': 'Say OK'}], 'max_tokens': 5}
        ))
    
    # Add more tests as needed
    
    results = await asyncio.gather(*tests, return_exceptions=True)
    
    successful = sum(1 for r in results if r is True)
    print(f"\n📊 Results: {successful}/{len(tests)} providers work with NEW keys")
    
    if successful > 0:
        print("🎉 Ready for business development!")
    else:
        print("⚠️  Configure at least one provider with a NEW key")

asyncio.run(test_all())

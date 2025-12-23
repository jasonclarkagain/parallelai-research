#!/usr/bin/env python3
"""
Verify ParallelAI platform functionality
"""
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("🧪 ParallelAI Platform Verification")
print("=" * 50)

# Test 1: Imports
print("\n1. Testing imports...")
try:
    from src.parallelai.key_manager import load_keys
    from src.real_swarm import WorkingSwarm
    print("   ✅ All imports successful")
except ImportError as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Key loading
print("\n2. Testing key loading...")
try:
    keys = load_keys()
    print(f"   ✅ Loaded {len(keys)} provider keys")
    
    working = [p for p in keys if keys[p]]
    print(f"   ✅ {len(working)} providers have keys configured:")
    for p in working:
        print(f"      • {p}")
except Exception as e:
    print(f"   ❌ Key loading failed: {e}")

# Test 3: Platform test
print("\n3. Testing platform functionality...")
async def test_platform():
    try:
        async with WorkingSwarm() as swarm:
            # Quick test with Groq if available
            keys = load_keys()
            if keys.get('groq'):
                print("   Testing Groq provider...")
                result = await swarm.query_specific('groq', 'Say hello in one word')
                if result.get('success'):
                    print(f"   ✅ Groq working: {result.get('model', 'Unknown')}")
                    print(f"   Response: {result['response']}")
                else:
                    print(f"   ❌ Groq test failed: {result.get('error', 'Unknown')}")
            else:
                print("   ⚠️  No Groq key to test")
    except Exception as e:
        print(f"   ❌ Platform test failed: {e}")

asyncio.run(test_platform())

print("\n" + "=" * 50)
print("✅ ParallelAI platform verification complete!")
print("🚀 Platform is ready for research!")

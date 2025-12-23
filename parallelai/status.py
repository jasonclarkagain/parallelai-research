#!/usr/bin/env python3
"""
Check status of all API providers
"""
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.parallelai.key_manager import load_keys
from src.real_swarm import WorkingSwarm

async def check_providers():
    """Check which providers are working"""
    keys = load_keys()
    
    print("🔍 ParallelAI Provider Status")
    print("=" * 50)
    
    # Check keys first
    print("\n🔑 API Keys Configured:")
    for provider in ['openai', 'anthropic', 'groq', 'together', 'openrouter']:
        if keys.get(provider):
            print(f"  ✅ {provider}: Configured")
        else:
            print(f"  ❌ {provider}: Not configured")
    
    # Test each provider
    print("\n🧪 Testing Providers (quick test)...")
    
    async with WorkingSwarm() as swarm:
        for provider in ['anthropic', 'groq', 'together', 'openrouter', 'openai']:
            if keys.get(provider):
                print(f"\n  Testing {provider}...", end='', flush=True)
                result = await swarm.query_specific(provider, "Say 'hello' in one word.")
                
                if result.get('success'):
                    print(f" ✅ WORKING")
                    print(f"     Model: {result.get('model', 'Unknown')}")
                else:
                    error = result.get('error', 'Unknown error')
                    if '401' in error or '403' in error:
                        print(f" ❌ AUTH ERROR")
                    elif '429' in error:
                        print(f" ⚠️  RATE LIMITED")
                    else:
                        print(f" ❌ ERROR: {error[:50]}...")
            else:
                print(f"\n  {provider}: ❌ No key configured")
    
    print("\n" + "=" * 50)
    print("🎯 READY FOR RESEARCH!")

if __name__ == "__main__":
    asyncio.run(check_providers())

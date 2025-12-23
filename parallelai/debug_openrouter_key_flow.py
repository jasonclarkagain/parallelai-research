#!/usr/bin/env python3
"""
Debug OpenRouter key flow from config to swarm
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 1. Check what's in the config file
print("🔍 STEP 1: Checking config file...")
config_file = Path.home() / '.parallelai' / 'config'
if config_file.exists():
    import configparser
    config = configparser.ConfigParser()
    config.read(config_file)
    
    if config.has_section('api_keys'):
        openrouter_key = config.get('api_keys', 'openrouter', fallback='NOT_FOUND')
        print(f"   Config file has openrouter key: {openrouter_key[:12]}... ({len(openrouter_key)} chars)")
    else:
        print("   ❌ No [api_keys] section in config")
else:
    print("   ❌ Config file not found")

# 2. Check what key_manager returns
print("\n🔍 STEP 2: Checking key_manager...")
try:
    from src.parallelai.key_manager import load_keys
    keys = load_keys()
    openrouter_from_manager = keys.get('openrouter', 'NOT_FOUND')
    print(f"   Key manager returns openrouter key: {openrouter_from_manager[:12] if openrouter_from_manager != 'NOT_FOUND' else 'NOT_FOUND'}...")
    print(f"   All keys from manager: {list(keys.keys())}")
except Exception as e:
    print(f"   ❌ Error loading keys: {e}")

# 3. Check what real_swarm sees
print("\n🔍 STEP 3: Checking real_swarm initialization...")
try:
    from src.real_swarm import WorkingSwarm
    swarm = WorkingSwarm()
    print(f"   Swarm keys: {list(swarm.keys.keys())}")
    print(f"   Swarm openrouter key present: {'openrouter' in swarm.keys}")
    if 'openrouter' in swarm.keys:
        print(f"   Swarm openrouter key: {swarm.keys['openrouter'][:12]}...")
except Exception as e:
    print(f"   ❌ Error checking swarm: {e}")

# 4. Direct API test with the key from config
print("\n🔍 STEP 4: Direct API test...")
import requests
if openrouter_key and openrouter_key != 'NOT_FOUND':
    headers = {
        "Authorization": f"Bearer {openrouter_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/parallelai-research/parallelai",
        "X-Title": "ParallelAI Research"
    }
    
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 10
    }
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=10
    )
    
    print(f"   Direct API status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Direct API works! Response: {response.json()['choices'][0]['message']['content']}")
    elif response.status_code == 401:
        print(f"   ❌ Direct API 401 - key is invalid for chat endpoint")
        print(f"   Response: {response.text[:200]}")
    else:
        print(f"   Response: {response.text[:200]}")
else:
    print("   ❌ No key to test")

print("\n📋 RECOMMENDATIONS:")
print("1. If direct API works but swarm doesn't: Key manager ↔ swarm mismatch")
print("2. If direct API also 401: Key invalid for chat (but valid for models)")
print("3. Check OpenRouter credits: https://openrouter.ai/credits")

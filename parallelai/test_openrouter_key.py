#!/usr/bin/env python3
import requests
import os
from pathlib import Path

# Try to get key from multiple sources
def get_openrouter_key():
    # 1. From config file
    config_file = Path.home() / '.parallelai' / 'config'
    if config_file.exists():
        import configparser
        config = configparser.ConfigParser()
        config.read(config_file)
        if config.has_section('api_keys'):
            key = config.get('api_keys', 'openrouter', fallback='')
            if key:
                return key
    
    # 2. From environment
    return os.getenv('OPENROUTER_API_KEY', '')

key = get_openrouter_key()
print(f"🔑 OpenRouter Key (masked): {key[:8]}...{key[-4:] if len(key) > 12 else '***'}")
print(f"📏 Key length: {len(key)} characters")

if not key:
    print("❌ No OpenRouter key found")
    exit(1)

# Test the key
headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://github.com/parallelai-research/parallelai",
    "X-Title": "ParallelAI Research"
}

print("\n🧪 Testing OpenRouter API...")

# Test 1: Models endpoint
response = requests.get("https://openrouter.ai/api/v1/models", headers=headers, timeout=10)
print(f"📊 Models endpoint status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"✅ API key valid! Available models:")
    for model in data['data'][:5]:  # Show first 5 models
        print(f"   • {model['id']}")
elif response.status_code == 401:
    print("❌ Invalid API key (401 Unauthorized)")
    print("💡 Possible reasons:")
    print("   1. Key is expired or invalid")
    print("   2. Need to add billing method at https://openrouter.ai/settings/keys")
    print("   3. Key format is wrong")
elif response.status_code == 429:
    print("⚠️ Rate limited (429)")
else:
    print(f"❌ Unexpected error: {response.text[:200]}")

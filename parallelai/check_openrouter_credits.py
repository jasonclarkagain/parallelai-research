#!/usr/bin/env python3
import requests
from pathlib import Path
import configparser

# Get OpenRouter key
config_file = Path.home() / '.parallelai' / 'config'
config = configparser.ConfigParser()
config.read(config_file)
openrouter_key = config.get('api_keys', 'openrouter', fallback='')

print("🔍 Checking OpenRouter account status...")

headers = {
    "Authorization": f"Bearer {openrouter_key}",
}

# Try to get credit balance (OpenRouter might not expose this via API)
# Instead, let's test with a very cheap/free model
payload = {
    "model": "google/gemini-3-flash-preview",  # Known free model
    "messages": [{"role": "user", "content": "Say hello"}],
    "max_tokens": 10
}

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers=headers,
    json=payload,
    timeout=15
)

print(f"Status: {response.status_code}")

if response.status_code == 200:
    print("✅ OpenRouter is working! You have credits.")
    data = response.json()
    print(f"Response: {data['choices'][0]['message']['content']}")
elif response.status_code == 402:
    print("❌ 402 Payment Required")
    print("💡 Visit: https://openrouter.ai/settings/billing")
    print("   Add a payment method to get started")
elif response.status_code == 401:
    print("❌ 401 Unauthorized - key might need refresh")
    print("💡 Visit: https://openrouter.ai/settings/keys")
    print("   Generate a new key")
else:
    print(f"❌ Error {response.status_code}: {response.text[:200]}")

print("\n💡 OpenRouter requires credits for most models.")
print("   Free options:")
print("   1. google/gemini-3-flash-preview")
print("   2. Some models marked as ':free'")
print("   3. Add $10 credit to unlock more models")

#!/usr/bin/env python3
import requests
import json
from pathlib import Path
import configparser

# Get OpenRouter key
config_file = Path.home() / '.parallelai' / 'config'
config = configparser.ConfigParser()
config.read(config_file)
openrouter_key = config.get('api_keys', 'openrouter', fallback='')

print(f"🔑 OpenRouter Key: {openrouter_key[:12]}...")
print(f"📏 Key length: {len(openrouter_key)}")

# Headers for OpenRouter
headers = {
    "Authorization": f"Bearer {openrouter_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://github.com/parallelai-research/parallelai",
    "X-Title": "ParallelAI Research"
}

# Test different models
test_models = [
    "openai/gpt-3.5-turbo",
    "meta-llama/llama-3-70b-instruct",
    "google/gemini-3-flash-preview",  # Free model
    "mistralai/mistral-small-creative",  # Another free option
]

for model in test_models:
    print(f"\n🧪 Testing model: {model}")
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Hello, testing OpenRouter"}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success! Response: {data['choices'][0]['message']['content'][:50]}...")
            print(f"   📊 Usage: {data.get('usage', {})}")
            break  # Found a working model!
        elif response.status_code == 401:
            error_data = response.json()
            print(f"   ❌ 401 Unauthorized: {error_data.get('error', {}).get('message', 'No error message')}")
        elif response.status_code == 402:
            print("   💰 402 Payment Required - need credits")
        elif response.status_code == 429:
            print("   ⚠️ 429 Rate Limited")
        else:
            print(f"   ❌ Error {response.status_code}: {response.text[:100]}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")

print("\n📋 Recommendations:")
print("1. Check your OpenRouter credits: https://openrouter.ai/credits")
print("2. Try a free model like 'google/gemini-3-flash-preview'")
print("3. Add billing method if needed: https://openrouter.ai/settings/billing")

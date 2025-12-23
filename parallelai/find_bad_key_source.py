#!/usr/bin/env python3
"""
Find where the invalid OpenRouter key is coming from
"""
import os
import sys
from pathlib import Path

print("🔍 Investigating OpenRouter key sources...")
print("=" * 50)

# Source 1: Config file
config_file = Path.home() / '.parallelai' / 'config'
print("\n1. Config file (~/.parallelai/config):")
if config_file.exists():
    import configparser
    config = configparser.ConfigParser()
    config.read(config_file)
    
    if config.has_section('api_keys'):
        config_key = config.get('api_keys', 'openrouter', fallback='NOT_SET')
        print(f"   Key: {config_key[:20]}...")
        print(f"   Length: {len(config_key)} chars")
    else:
        print("   ❌ No [api_keys] section")
else:
    print("   ❌ File not found")

# Source 2: Environment variable
print("\n2. Environment variable (OPENROUTER_API_KEY):")
env_key = os.getenv('OPENROUTER_API_KEY', 'NOT_SET')
print(f"   Key: {env_key[:20] if env_key != 'NOT_SET' else 'NOT_SET'}...")
print(f"   Length: {len(env_key) if env_key != 'NOT_SET' else 0} chars")

# Source 3: Any other files key_manager might check
print("\n3. Checking common key file locations:")
key_locations = [
    Path.home() / '.api_keys' / 'openrouter.key',
    Path.home() / '.api_keys' / 'openrouter',
    Path.home() / 'openrouter_key.txt',
    Path.home() / '.openrouter_key',
]

for loc in key_locations:
    if loc.exists():
        try:
            with open(loc, 'r') as f:
                key = f.read().strip()
                print(f"   Found in {loc}: {key[:20]}... ({len(key)} chars)")
        except:
            pass

# Source 4: Check if key_manager has cached something
print("\n4. Simulating what key_manager.load_keys() does:")

def simulate_load_keys():
    keys = {}
    
    # Environment variables (priority 1)
    env_keys = {
        'openai': os.getenv('OPENAI_API_KEY'),
        'anthropic': os.getenv('ANTHROPIC_API_KEY'),
        'groq': os.getenv('GROQ_API_KEY'),
        'together': os.getenv('TOGETHER_API_KEY'),
        'openrouter': os.getenv('OPENROUTER_API_KEY'),
    }
    
    for provider, key in env_keys.items():
        if key:
            keys[provider] = key
    
    # Config file (priority 2)
    if config_file.exists():
        import configparser
        config = configparser.ConfigParser()
        config.read(config_file)
        
        if config.has_section('api_keys'):
            for provider, key in config.items('api_keys'):
                if key and (provider not in keys or not keys[provider]):
                    keys[provider] = key
    
    return keys

simulated_keys = simulate_load_keys()
print(f"   Simulated openrouter key: {simulated_keys.get('openrouter', 'NOT_FOUND')[:20] if simulated_keys.get('openrouter') else 'NOT_FOUND'}...")

print("\n🎯 RECOMMENDATION:")
print("   Clear environment variables that might override your config file:")
print("   unset OPENROUTER_API_KEY")
print("   Then test again: ./parallelai query --provider openrouter 'Test'")

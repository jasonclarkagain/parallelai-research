#!/usr/bin/env python3
"""
Debug script to check imports
"""
import sys
import os

print("🔍 Debugging ParallelAI Imports")
print("=" * 40)

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print(f"Current directory: {current_dir}")
print(f"Python path: {sys.path[:3]}")

print("\n1. Checking src directory...")
if os.path.exists("src"):
    print("✅ src directory exists")
    print(f"Contents: {os.listdir('src')}")
else:
    print("❌ src directory not found!")

print("\n2. Checking config.py...")
if os.path.exists("src/config.py"):
    print("✅ config.py exists")
    
    # Read config.py to see what's in it
    with open("src/config.py", 'r') as f:
        content = f.read()
    
    # Check for key variables
    variables_to_check = ['API_KEYS', 'API_ENDPOINTS', 'DEFAULT_MODELS', 'get_headers', 'HEADERS']
    for var in variables_to_check:
        if var in content:
            print(f"   ✅ {var} found in config.py")
        else:
            print(f"   ❌ {var} NOT found in config.py")
else:
    print("❌ config.py not found!")

print("\n3. Trying to import config...")
try:
    import src.config as config
    print("✅ Imported config module")
    print(f"Available attributes: {[attr for attr in dir(config) if not attr.startswith('_')][:10]}")
    
    # Try to access specific attributes
    try:
        endpoints = config.API_ENDPOINTS
        print(f"✅ API_ENDPOINTS: {list(endpoints.keys())[:3]}...")
    except:
        print("❌ API_ENDPOINTS not accessible")
    
    try:
        models = config.DEFAULT_MODELS
        print(f"✅ DEFAULT_MODELS: {list(models.keys())[:3]}...")
    except:
        print("❌ DEFAULT_MODELS not accessible")
    
    try:
        headers_func = config.get_headers
        print(f"✅ get_headers function: {headers_func}")
    except:
        print("❌ get_headers not accessible")
        
except Exception as e:
    print(f"❌ Failed to import config: {e}")
    import traceback
    traceback.print_exc()

print("\n4. Trying to import real_swarm...")
try:
    from src.real_swarm import WorkingSwarm
    print("✅ Successfully imported WorkingSwarm")
    print("✅ All imports working!")
except Exception as e:
    print(f"❌ Failed to import real_swarm: {e}")
    import traceback
    traceback.print_exc()

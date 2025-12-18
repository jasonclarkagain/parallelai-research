import os
import sys

print("🚀 PARALLELAI ULTIMATE SECURITY TEST")
print("=" * 50)

keys = {
    'GROQ_API_KEY': {
        'min_len': 40,
        'max_len': 60,
        'pattern': 'gsk_'
    },
    'TOGETHER_API_KEY': {
        'min_len': 50, 
        'max_len': 70,
        'pattern': None
    },
    'OPENROUTER_API_KEY': {
        'min_len': 50,
        'max_len': 70,
        'pattern': 'sk-or-'
    }
}

all_pass = True
for key_name, specs in keys.items():
    value = os.getenv(key_name, '')
    
    # Check if set
    if not value:
        print(f"❌ {key_name}: NOT SET")
        all_pass = False
        continue
    
    # Check length
    if len(value) < specs['min_len']:
        print(f"❌ {key_name}: Too short ({len(value)} < {specs['min_len']})")
        all_pass = False
        continue
    elif len(value) > specs['max_len']:
        print(f"⚠️  {key_name}: Long ({len(value)} > {specs['max_len']})")
    
    # Check pattern
    if specs['pattern'] and not value.startswith(specs['pattern']):
        print(f"⚠️  {key_name}: Doesn't match pattern '{specs['pattern']}'")
    
    # Check for placeholders
    forbidden = ['YOUR_', 'ACTUAL', 'PLACEHOLDER', 'EXAMPLE', 'TEST']
    if any(f.upper() in value.upper() for f in forbidden):
        print(f"❌ {key_name}: Contains placeholder text")
        all_pass = False
        continue
    
    print(f"✅ {key_name}: Valid ({len(value)} chars)")

print("=" * 50)
if all_pass:
    print("🎉 ALL SYSTEMS GO! Ready to launch ParallelAI business.")
    print("   Run: python src/swarm_router.py")
else:
    print("⚠️  Issues detected. Generate REAL API keys from providers.")
    sys.exit(1)

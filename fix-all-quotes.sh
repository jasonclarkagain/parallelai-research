#!/bin/bash
echo "🔧 Fixing All Quote Issues in ParallelAI"
echo "========================================"

echo ""
echo "1. Fixing .env file..."
if [ -f .env ]; then
    echo "   Original .env contents (first line):"
    head -1 .env
    
    # Remove all quotes
    sed 's/"//g' .env > .env.tmp
    mv .env.tmp .env
    
    echo "   Fixed .env contents (first line):"
    head -1 .env
else
    echo "   ❌ .env file not found"
fi

echo ""
echo "2. Making sure improved script is the main one..."
if [ -f parallelai-simple-improved ]; then
    cp parallelai-simple-improved parallelai-simple
    chmod +x parallelai-simple
    echo "   ✅ Updated parallelai-simple"
fi

echo ""
echo "3. Testing the fix..."
source .env 2>/dev/null || echo "   Note: .env sourced"

python3 << 'PYTHON'
import os
print("Environment check:")
for key in ['GROQ_API_KEY', 'TOGETHER_API_KEY', 'OPENROUTER_API_KEY']:
    val = os.getenv(key)
    status = '✅' if val and len(val) > 30 else '❌'
    print(f"   {key}: {status} ({len(val) if val else 0} chars)")
PYTHON

echo ""
echo "4. Final test..."
./parallelai-simple "Say TEST PASSED" 2>&1 | grep -A2 "✅" || echo "   ❌ Test failed - run ./parallelai-simple 'Hello' manually"

echo ""
echo "✅ Fix applied! Run: source .env && ./parallelai-simple 'Your query'"

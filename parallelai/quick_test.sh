#!/bin/bash

echo "🧪 Testing ParallelAI Setup"
echo "==========================="

# Test 1: Check parallelai executable
echo -n "1. Checking parallelai executable... "
if [ -f "parallelai" ] && [ -x "parallelai" ]; then
    echo "✅"
else
    echo "❌"
    echo "   Make sure parallelai exists and is executable"
    exit 1
fi

# Test 2: Check Python modules
echo -n "2. Checking Python dependencies... "
python3 -c "import aiohttp, asyncio" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅"
else
    echo "❌"
    echo "   Install dependencies: pip install aiohttp"
    exit 1
fi

# Test 3: Check API keys
echo -n "3. Checking API keys... "
./parallelai keys list > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅"
else
    echo "⚠️"
    echo "   Run: ./setup_keys.sh"
fi

echo ""
echo "🚀 Ready to use ParallelAI!"
echo "   Try: ./parallelai query 'Explain AI in one sentence'"

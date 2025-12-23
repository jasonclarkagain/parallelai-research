#!/bin/bash

echo "🔧 OpenRouter Troubleshooting Guide"
echo "==================================="
echo ""
echo "OpenRouter returned 401 (Unauthorized). Let's fix it:"
echo ""

# Step 1: Check current key
echo "1. Checking current OpenRouter key..."
if [ -f ~/.parallelai/config ]; then
    OPENROUTER_KEY=$(grep -A 5 '\[api_keys\]' ~/.parallelai/config | grep 'openrouter' | cut -d'=' -f2 | xargs)
    if [ -n "$OPENROUTER_KEY" ]; then
        echo "   ✅ Key found: ${OPENROUTER_KEY:0:8}...${OPENROUTER_KEY: -4}"
        echo "   📏 Length: ${#OPENROUTER_KEY} characters"
    else
        echo "   ❌ No OpenRouter key in config"
    fi
else
    echo "   ❌ Config file not found"
fi

echo ""
echo "2. Manual test of OpenRouter API..."
echo "   (Running Python test script)"
python3 test_openrouter_key.py

echo ""
echo "3. Solutions:"
echo ""
echo "   💡 OPTION A: Get a new OpenRouter key"
echo "     1. Visit: https://openrouter.ai/settings/keys"
echo "     2. Create a new API key"
echo "     3. Update your config:"
echo "        ./parallelai keys set --provider openrouter"
echo ""
echo "   💡 OPTION B: Use a different model (already configured)"
echo "     OpenRouter now uses 'openai/gpt-3.5-turbo' which is more reliable"
echo ""
echo "   💡 OPTION C: Check OpenRouter status"
echo "     - Visit: https://openrouter.ai/status"
echo "     - Check if API is operational"
echo "     - Ensure you have credits"
echo ""
echo "4. Quick fix - update OpenRouter key:"
read -p "   Do you want to update your OpenRouter key now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ./parallelai keys set --provider openrouter
fi

echo ""
echo "5. After fixing, test again:"
echo "   ./parallelai query --provider openrouter 'Test OpenRouter'"

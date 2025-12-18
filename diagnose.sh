#!/bin/bash
echo "🩺 ParallelAI Diagnostic Tool"
echo "============================="

echo ""
echo "1. Checking .env file..."
if [ -f .env ]; then
    echo "✅ .env file exists"
    # Show first few chars of each key (for debugging)
    grep -E "(GROQ|TOGETHER|OPENROUTER)_API_KEY" .env | while read line; do
        key=$(echo "$line" | cut -d'=' -f1)
        value=$(echo "$line" | cut -d'=' -f2-)
        len=${#value}
        echo "   $key: ${len} chars (starts with: ${value:0:8}...)"
    done
else
    echo "❌ .env file missing!"
fi

echo ""
echo "2. Checking environment variables..."
for key in GROQ_API_KEY TOGETHER_API_KEY OPENROUTER_API_KEY; do
    if [ -n "${!key}" ]; then
        len=${#!key}
        echo "   ✅ $key is set (${len} chars)"
    else
        echo "   ❌ $key is NOT set in environment"
    fi
done

echo ""
echo "3. Testing API endpoints..."
if [ -n "$GROQ_API_KEY" ]; then
    echo "   Testing Groq..."
    curl -s -o /tmp/groq_test.json -w "HTTP %{http_code}" \
         -H "Authorization: Bearer $GROQ_API_KEY" \
         -H "Content-Type: application/json" \
         -d '{"model":"llama-3.3-70b-versatile","messages":[{"role":"user","content":"Hi"}],"max_tokens":5}' \
         https://api.groq.com/openai/v1/chat/completions
    echo " response"
    if [ -f /tmp/groq_test.json ]; then
        if grep -q "error" /tmp/groq_test.json; then
            echo "   ❌ Groq API error: $(cat /tmp/groq_test.json | grep -o '"message":"[^"]*"' | head -1)"
        else
            echo "   ✅ Groq API working"
        fi
        rm /tmp/groq_test.json
    fi
fi

echo ""
echo "4. Testing Python import..."
python3 << 'PYTHON'
import os
print("Python environment check:")
print(f"  GROQ_API_KEY in os.environ: {'✅' if 'GROQ_API_KEY' in os.environ else '❌'}")
print(f"  TOGETHER_API_KEY in os.environ: {'✅' if 'TOGETHER_API_KEY' in os.environ else '❌'}")
print(f"  OPENROUTER_API_KEY in os.environ: {'✅' if 'OPENROUTER_API_KEY' in os.environ else '❌'}")

# Try to import requests
try:
    import requests
    print("  ✅ requests module available")
except:
    print("  ❌ requests module not installed")
PYTHON

echo ""
echo "📋 Summary:"
echo "   Run: source .env  to load API keys"
echo "   Then test with: ./parallelai-simple 'Hello'"

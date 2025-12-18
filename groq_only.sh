#!/bin/bash
cd ~/projects/parallelai
source .env

echo "🧪 Testing Groq API only..."
curl -s -X POST \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"llama-3.3-70b-versatile","messages":[{"role":"user","content":"Say TEST OK"}],"max_tokens":5}' \
  https://api.groq.com/openai/v1/chat/completions | grep -o '"content":"[^"]*"'

if [ $? -eq 0 ]; then
    echo "✅ Groq API is working!"
else
    echo "❌ Groq API failed. Check:"
    echo "   1. Key validity: https://console.groq.com/keys"
    echo "   2. Key format: Should start with 'gsk_' and be ~48 chars"
    echo "   3. Account status: May need email verification"
fi

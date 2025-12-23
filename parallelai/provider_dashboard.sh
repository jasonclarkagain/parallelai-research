#!/bin/bash
echo "📊 PARALLELAI PROVIDER DASHBOARD"
echo "================================"
echo "Generated: $(date)"
echo ""

# Check config file
echo "🔧 CONFIGURATION STATUS:"
echo "-----------------------"
if [ -f ~/.parallelai/config ]; then
    echo "✅ Config file exists"
    KEYS_COUNT=$(grep -c "=" ~/.parallelai/config | tail -1)
    echo "📋 $KEYS_COUNT keys configured"
else
    echo "❌ Config file missing"
fi

echo ""
echo "🚀 PROVIDER STATUS:"
echo "------------------"

# Test each provider
providers=("openai" "anthropic" "groq" "together" "openrouter")
for provider in "${providers[@]}"; do
    echo -n "🔍 $provider: "
    
    # Quick test with timeout
    timeout 15 ./parallelai query --provider "$provider" "Say 'ok'" 2>/dev/null > /tmp/provider_test_$$.txt
    
    if grep -q "✅ $provider" /tmp/provider_test_$$.txt 2>/dev/null; then
        echo "✅ WORKING"
        # Extract model info if available
        MODEL=$(grep "Model:" /tmp/provider_test_$$.txt | head -1 | cut -d: -f2 | xargs)
        [ -n "$MODEL" ] && echo "   📦 Using: $MODEL"
    elif grep -q "429" /tmp/provider_test_$$.txt 2>/dev/null; then
        echo "⚠️  RATE LIMITED"
    elif grep -q "401\|403" /tmp/provider_test_$$.txt 2>/dev/null; then
        echo "🔐 AUTH ERROR"
        echo "   💡 Run: ./parallelai keys set $provider YOUR_KEY"
    elif grep -q "❌ $provider" /tmp/provider_test_$$.txt 2>/dev/null; then
        echo "❌ ERROR"
    else
        echo "⏳ NO RESPONSE"
    fi
    
    rm -f /tmp/provider_test_$$.txt
done

echo ""
echo "🎯 QUICK ACTIONS:"
echo "----------------"
echo "1. Update Groq key:   ./parallelai keys set groq YOUR_KEY"
echo "2. Test all:          ./parallelai query 'Test message'"
echo "3. View keys:         ./parallelai keys list"
echo "4. Setup new:         ./parallelai keys setup"
echo ""
echo "📈 WORKING PROVIDERS: $(./parallelai query "test" 2>/dev/null | grep -c "✅")/5"

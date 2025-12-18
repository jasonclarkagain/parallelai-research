#!/bin/bash
echo "🔐 FINAL SECURITY AUDIT"
echo "========================"

# Load environment
cd ~/projects/parallelai
source .env 2>/dev/null

# 1. Vault status
echo "1. VAULT STATUS:"
if mountpoint -q ~/Vault; then
    echo "   ✅ Mounted"
    echo "   Files: $(ls ~/Vault/*.txt 2>/dev/null | wc -l)"
else
    echo "   🔒 Not mounted"
fi

# 2. Key validation
echo "2. API KEY VALIDATION:"
declare -A key_info
key_info[GROQ_API_KEY]="Should start with 'gsk_' (40-60 chars)"
key_info[TOGETHER_API_KEY]="Hex string (50-70 chars)"  
key_info[OPENROUTER_API_KEY]="Should start with 'sk-or-' (50-70 chars)"

all_valid=true
for key in "${!key_info[@]}"; do
    value="${!key}"
    if [ -z "$value" ]; then
        echo "   ❌ $key: NOT SET"
        all_valid=false
    elif [[ "$value" == *"YOUR_"* ]] || [[ "$value" == *"ACTUAL"* ]] || [[ "$value" == *"PLACEHOLDER"* ]]; then
        echo "   ⚠️  $key: Contains placeholder text (${#value} chars)"
        echo "      ${key_info[$key]}"
        all_valid=false
    elif [ ${#value} -lt 20 ]; then
        echo "   ⚠️  $key: Too short (${#value} chars)"
        echo "      ${key_info[$key]}"
        all_valid=false
    else
        echo "   ✅ $key: Valid (${#value} chars)"
    fi
done

# 3. Environment security
echo "3. ENVIRONMENT SECURITY:"
echo "   .env in .gitignore: $(grep -q "^\.env$" .gitignore && echo "✅" || echo "❌")"
echo "   .env permissions: $(stat -c "%A" .env)"

echo "================================"
if $all_valid; then
    echo "🎉 SECURE AND READY FOR PRODUCTION"
    exit 0
else
    echo "⚠️  SECURITY ISSUES DETECTED"
    echo "   Generate REAL API keys and update vault"
    exit 1
fi

#!/bin/bash
echo "=== FINAL SECURITY AUDIT ==="
echo "1. Environment Variables:"
env | grep -E "GROQ|TOGETHER|OPENROUTER" || echo "   (None found in environment - GOOD)"

echo "2. Vault Status:"
if mountpoint -q ~/Vault; then
    echo "   ✅ Mounted at ~/Vault"
    echo "   Files in vault:" $(ls ~/Vault/*.txt 2>/dev/null | wc -l)
else
    echo "   🔒 Not mounted (secure when not in use)"
fi

echo "3. .env File Permissions:"
ls -la .env | awk '{print "   Permissions: "$1" Owner: "$3}'

echo "4. Key Length Verification:"
source .env 2>/dev/null
for key in GROQ_API_KEY TOGETHER_API_KEY OPENROUTER_API_KEY; do
    len=${#!key}
    if [ $len -gt 20 ]; then
        echo "   ✅ $key: $len chars (looks valid)"
    elif [ $len -gt 0 ]; then
        echo "   ⚠️  $key: Only $len chars (might be placeholder)"
    else
        echo "   ❌ $key: Not set"
    fi
done
echo "=== AUDIT COMPLETE ==="

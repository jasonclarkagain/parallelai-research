#!/bin/bash
echo "🔍 Secret Check Before Push"
echo "=========================="

echo ""
echo "1. Checking current commit for API keys..."
if git show | grep -E "(gsk_|tgp_|sk-or-)" | grep -v "your_key"; then
    echo "❌ API keys found in commit!"
    git show | grep -B2 -A2 -E "(gsk_|tgp_|sk-or-)" | grep -v "your_key"
else
    echo "✅ No API keys found in commit"
fi

echo ""
echo "2. Checking tracked files for secrets..."
TRACKED_FILES=$(git ls-files)
for file in $TRACKED_FILES; do
    if [ -f "$file" ]; then
        if grep -q -E "(gsk_|tgp_|sk-or-)" "$file" 2>/dev/null; then
            echo "❌ Secret in tracked file: $file"
            grep -n -E "(gsk_|tgp_|sk-or-)" "$file" | head -3
        fi
    fi
done

echo ""
echo "3. Files that will be pushed:"
git ls-files | head -20

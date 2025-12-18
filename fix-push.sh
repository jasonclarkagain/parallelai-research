#!/bin/bash
echo "🔄 Fixing Git Push Issues"
echo "========================"

echo ""
echo "1. Checking remote status..."
git fetch origin

echo ""
echo "2. Trying to pull and merge..."
if git pull origin main --no-rebase; then
    echo "✅ Pull successful!"
    echo ""
    echo "3. Now pushing..."
    git push origin main
else
    echo "❌ Pull failed (likely conflicts)"
    echo ""
    echo "💡 Options:"
    echo "   A. Force push (overwrites remote):"
    echo "      git push origin main --force-with-lease"
    echo ""
    echo "   B. Create fresh branch and PR:"
    echo "      git checkout -b fix/auto-env"
    echo "      git push origin fix/auto-env"
    echo "      # Then create PR on GitHub"
    echo ""
    echo "   C. Reset and start fresh:"
    echo "      git fetch origin"
    echo "      git reset --hard origin/main"
    echo "      # WARNING: This discards local changes!"
fi

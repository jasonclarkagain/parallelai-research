#!/bin/bash
echo "🚀 GitHub Update Script for ParallelAI"
echo "====================================="

# Get commit message
if [ -z "$1" ]; then
    echo "Enter commit message (or press Enter for default):"
    read COMMIT_MSG
    if [ -z "$COMMIT_MSG" ]; then
        COMMIT_MSG="feat: Update ParallelAI with working providers"
    fi
else
    COMMIT_MSG="$1"
fi

echo ""
echo "📊 Git Status:"
git status --short

echo ""
echo "📦 Staging changes..."
git add .

echo ""
echo "💾 Committing with message:"
echo "   '$COMMIT_MSG'"
git commit -m "$COMMIT_MSG"

echo ""
echo "📤 Pushing to GitHub..."
git push origin master

echo ""
echo "✅ GitHub update complete!"
echo "🔗 Check your repository at: https://github.com/YOUR_USERNAME/parallelai"

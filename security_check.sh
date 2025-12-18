#!/bin/bash
echo "🔒 Security Check Before Git Commit"
echo "==================================="

echo ""
echo "1. Checking for API keys in files..."
FOUND_KEYS=0

# Check for Groq keys
if grep -r "gsk_[a-zA-Z0-9]" . --include="*.py" --include="*.sh" --include="*.txt" --include="*.md" 2>/dev/null | grep -v ".env.example" | grep -v "your_groq_key"; then
    echo "❌ GROQ API keys found in source files!"
    grep -r "gsk_" . --include="*.py" --include="*.sh" --include="*.txt" --include="*.md" 2>/dev/null | grep -v ".env.example" | grep -v "your_groq_key"
    FOUND_KEYS=1
fi

# Check for Together keys
if grep -r "tgp_[a-zA-Z0-9]" . --include="*.py" --include="*.sh" --include="*.txt" --include="*.md" 2>/dev/null | grep -v ".env.example" | grep -v "your_together_key"; then
    echo "❌ Together AI API keys found in source files!"
    grep -r "tgp_" . --include="*.py" --include="*.sh" --include="*.txt" --include="*.md" 2>/dev/null | grep -v ".env.example" | grep -v "your_together_key"
    FOUND_KEYS=1
fi

# Check for OpenRouter keys
if grep -r "sk-or-[a-zA-Z0-9]" . --include="*.py" --include="*.sh" --include="*.txt" --include="*.md" 2>/dev/null | grep -v ".env.example" | grep -v "your_openrouter_key"; then
    echo "❌ OpenRouter API keys found in source files!"
    grep -r "sk-or-" . --include="*.py" --include="*.sh" --include="*.txt" --include="*.md" 2>/dev/null | grep -v ".env.example" | grep -v "your_openrouter_key" 
    FOUND_KEYS=1
fi

if [ $FOUND_KEYS -eq 0 ]; then
    echo "✅ No API keys found in source files"
fi

echo ""
echo "2. Checking .gitignore..."
if grep -q "\.env" .gitignore; then
    echo "✅ .env is in .gitignore"
else
    echo "❌ .env is NOT in .gitignore - Adding it now"
    echo ".env" >> .gitignore
fi

if [ -f .env ]; then
    echo "⚠️  WARNING: .env file exists with your real keys."
    echo "   This file should NOT be committed to Git!"
    echo "   Make sure it's listed in .gitignore"
fi

echo ""
echo "3. Checking file permissions..."
if [ -x "parallelai-simple" ]; then
    echo "✅ parallelai-simple is executable"
else
    echo "⚠️  parallelai-simple is not executable"
fi

echo ""
if [ $FOUND_KEYS -eq 0 ]; then
    echo "✅ Security check PASSED - Safe to commit"
else
    echo "❌ Security check FAILED - Fix issues before committing!"
    echo "   Remove API keys from all files except .env"
    exit 1
fi

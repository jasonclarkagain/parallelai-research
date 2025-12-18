#!/bin/bash
echo "🚀 Complete ParallelAI Setup"
echo "============================"

cd ~/projects/parallelai

# 1. Ensure .env exists
if [ ! -f .env ]; then
    echo "Creating .env file with current environment..."
    cat > .env << EOL
# ParallelAI API Keys (auto-detected from environment)
GROQ_API_KEY="${GROQ_API_KEY}"
TOGETHER_API_KEY="${TOGETHER_API_KEY}"
OPENROUTER_API_KEY="${OPENROUTER_API_KEY}"
EOL
    echo "✅ Created .env file"
fi

# 2. Install the simple reliable version
echo "Installing simple CLI (most reliable)..."
sudo cp parallelai-simple /usr/local/bin/parallelai 2>/dev/null || true

# 3. Create helper script
cat > ~/projects/parallelai/quick-test.sh << 'EOQ'
#!/bin/bash
echo "🧪 Quick ParallelAI Test"
echo "========================"
echo "1. Testing fast mode:"
parallelai-simple "Say TEST PASSED" 2>/dev/null | grep -A5 "✅" || echo "   ❌ Fast mode failed"
echo ""
echo "2. Testing all mode:"
parallelai-simple --all "Say OK" 2>/dev/null | grep -B2 -A2 "✅" | head -20 || echo "   ❌ All mode failed"
echo ""
echo "3. Configuration check:"
ls -la ~/projects/parallelai/.env
echo ""
echo "✅ Setup complete!"
echo "💡 Usage: parallelai-simple \"your question here\""
EOQ

chmod +x ~/projects/parallelai/quick-test.sh

# 4. Create a universal pai command
sudo tee /usr/local/bin/pai << 'PAI_EOF' > /dev/null
#!/bin/bash
# Universal pai command - uses the most reliable backend
if [ "$1" = "--all" ]; then
    shift
    exec parallelai-simple --all "$@"
else
    exec parallelai-simple "$@"
fi
PAI_EOF

sudo chmod +x /usr/local/bin/pai

# 5. Update bashrc
if ! grep -q "alias pai=" ~/.bashrc 2>/dev/null; then
    echo "alias pai='parallelai-simple'" >> ~/.bashrc
fi

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "📦 Available Commands:"
echo "   • parallelai-simple  - Most reliable (sequential fallback)"
echo "   • pai                - Universal command (recommended)"
echo "   • parallelai2        - Async version with --all flag"
echo ""
echo "🧪 Run tests:"
echo "   ~/projects/parallelai/quick-test.sh"
echo ""
echo "🚀 Quick start:"
echo "   pai \"Explain quantum computing\""
echo "   pai --all \"Write Python code for web scraper\""

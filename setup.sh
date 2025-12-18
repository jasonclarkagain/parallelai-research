#!/bin/bash
echo "🚀 ParallelAI CLI Setup"
echo "======================"

echo ""
echo "📦 Checking dependencies..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is required but not installed."
    echo "   Install with: sudo apt install python3"
    exit 1
fi

if ! python3 -c "import requests" 2>/dev/null; then
    echo "📦 Installing required Python packages..."
    pip3 install requests || pip install requests || echo "⚠️  Could not install requests automatically"
fi

echo ""
echo "🔧 Setting up API keys..."
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Created .env file from template"
        echo ""
        echo "📝 Please edit .env and add your API keys:"
        echo "   - Groq: https://console.groq.com"
        echo "   - Together AI: https://api.together.xyz"  
        echo "   - OpenRouter: https://openrouter.ai"
        echo ""
        echo "💡 Run: nano .env  (or use your favorite editor)"
    else
        echo "❌ .env.example not found. Creating basic .env..."
        cat > .env << 'EOENV'
# ParallelAI API Keys
GROQ_API_KEY=""
TOGETHER_API_KEY=""
OPENROUTER_API_KEY=""
EOENV
        echo "✅ Created .env file. Please add your API keys."
    fi
else
    echo "✅ .env file already exists"
fi

echo ""
echo "⚡ Making scripts executable..."
chmod +x parallelai-simple parallelai parallelai-v2 2>/dev/null || true
chmod +x scripts/*.sh 2>/dev/null || true

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Quick Start:"
echo "   1. Add your API keys to .env file"
echo "   2. Run: source .env"
echo "   3. Test: ./parallelai-simple \"Hello, world!\""
echo ""
echo "💡 Pro Tips:"
echo "   - Use './parallelai-simple --all' to compare all providers"
echo "   - Check './scripts/quick-test.sh' for a system test"
echo "   - Run './scripts/manage_config.sh help' for key management"

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

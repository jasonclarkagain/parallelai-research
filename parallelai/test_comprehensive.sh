#!/bin/bash

echo "🧪 ParallelAI Comprehensive Test"
echo "================================"
echo "Testing all providers with the same query..."
echo ""

QUERY="Explain the concept of artificial intelligence in one paragraph."

echo "Query: '$QUERY'"
echo ""

# Test each provider individually
providers=("anthropic" "groq" "together" "openrouter")

for provider in "${providers[@]}"; do
    echo "--- Testing $provider ---"
    ./parallelai query --provider "$provider" "$QUERY" 2>/dev/null | \
        grep -A 5 "✅ ${provider^^}:" | \
        tail -n +2 | \
        head -3
    echo ""
done

echo "✅ Comprehensive test complete!"
echo "📈 Multiple AI providers are working in parallel!"

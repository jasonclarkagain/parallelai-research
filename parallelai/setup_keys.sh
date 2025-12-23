#!/bin/bash

echo "🔐 ParallelAI API Key Setup"
echo "==========================="
echo ""

# Check if parallelai exists
if [ ! -f "parallelai" ]; then
    echo "❌ parallelai not found in current directory"
    echo "💡 Make sure you're in the parallelai directory"
    exit 1
fi

echo "Options:"
echo "1. Interactive setup (recommended)"
echo "2. Migrate from existing files"
echo "3. List current keys"
echo "4. Test keys"
echo "5. Exit"
echo ""

read -p "Choose option (1-5): " choice

case $choice in
    1)
        ./parallelai keys setup
        ;;
    2)
        ./parallelai keys migrate
        ;;
    3)
        ./parallelai keys list
        ;;
    4)
        ./parallelai keys test
        ;;
    5)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "📋 Next steps:"
echo "   Test your setup: ./parallelai query 'Hello, how are you?'"

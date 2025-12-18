#!/bin/bash
echo "🔐 ParallelAI Configuration Manager"
echo "==================================="

CONFIG_DIR="$HOME/projects/parallelai"
ENV_FILE="$CONFIG_DIR/.env"

if [ ! -d "$CONFIG_DIR" ]; then
    echo "Creating directory: $CONFIG_DIR"
    mkdir -p "$CONFIG_DIR"
fi

case "$1" in
    "set")
        echo "Setting API keys..."
        echo ""
        read -p "Enter GROQ_API_KEY: " GROQ_KEY
        read -p "Enter TOGETHER_API_KEY: " TOGETHER_KEY
        read -p "Enter OPENROUTER_API_KEY: " OPENROUTER_KEY
        
        cat > "$ENV_FILE" << EOL
# ParallelAI API Keys
GROQ_API_KEY="$GROQ_KEY"
TOGETHER_API_KEY="$TOGETHER_KEY"
OPENROUTER_API_KEY="$OPENROUTER_KEY"

# Optional: Set default model preferences
# DEFAULT_MODEL_GROQ="llama-3.3-70b-versatile"
# DEFAULT_MODEL_TOGETHER="mistralai/Mixtral-8x7B-Instruct-v0.1"
# DEFAULT_MODEL_OPENROUTER="mistralai/mistral-7b-instruct:free"
EOL
        echo "✅ Keys saved to $ENV_FILE"
        ;;
        
    "show")
        echo "Current configuration:"
        echo "======================"
        if [ -f "$ENV_FILE" ]; then
            # Show keys with first/last few chars for security
            while IFS='=' read -r key value; do
                if [[ "$key" == *KEY* ]]; then
                    val=${value//\"/}
                    len=${#val}
                    if [ $len -gt 8 ]; then
                        masked="${val:0:4}...${val: -4}"
                    else
                        masked="[too short]"
                    fi
                    echo "$key=$masked"
                fi
            done < "$ENV_FILE"
        else
            echo "No configuration file found at $ENV_FILE"
            echo "Run: $0 set"
        fi
        ;;
        
    "test")
        echo "Testing all providers..."
        source "$ENV_FILE"
        
        if command -v parallelai2 &> /dev/null; then
            parallelai2 --all "Say TEST OK in one word"
        elif command -v parallelai &> /dev/null; then
            parallelai "Say TEST OK in one word"
        else
            echo "ParallelAI CLI not found. Run install_parallelai.sh first"
        fi
        ;;
        
    "check")
        echo "Provider status:"
        echo "================"
        if [ -f "$ENV_FILE" ]; then
            source "$ENV_FILE"
            echo -n "Groq: "
            curl -s -o /dev/null -w "%{http_code}" \
                 -H "Authorization: Bearer $GROQ_API_KEY" \
                 https://api.groq.com/openai/v1/models > /dev/null 2>&1
            echo " (200 means OK)"
            
            echo -n "Together: "
            curl -s -o /dev/null -w "%{http_code}" \
                 -H "Authorization: Bearer $TOGETHER_API_KEY" \
                 https://api.together.xyz/v1/models > /dev/null 2>&1
            echo " (200 means OK)"
        else
            echo "No .env file found"
        fi
        ;;
        
    *)
        echo "Usage: $0 {set|show|test|check}"
        echo ""
        echo "Commands:"
        echo "  set    - Set API keys interactively"
        echo "  show   - Show current configuration"
        echo "  test   - Test all providers"
        echo "  check  - Quick health check"
        exit 1
        ;;
esac

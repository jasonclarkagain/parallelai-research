#!/bin/bash

echo "🔄 Manual OpenRouter Key Reset"
echo "=============================="

# Backup current config
BACKUP_FILE="$HOME/.parallelai/config.backup.$(date +%s)"
cp "$HOME/.parallelai/config" "$BACKUP_FILE" 2>/dev/null || true
echo "📦 Backup created: $BACKUP_FILE"

# Show current key
echo ""
echo "Current OpenRouter key in config:"
grep -A 5 '\[api_keys\]' "$HOME/.parallelai/config" | grep 'openrouter' | head -1

echo ""
read -p "Do you want to: (1) Enter new key, (2) Delete key, (3) Cancel [1/2/3]: " choice

case $choice in
    1)
        echo ""
        echo "Get a new OpenRouter key from: https://openrouter.ai/settings/keys"
        echo ""
        read -p "Enter new OpenRouter key: " new_key
        if [ -n "$new_key" ]; then
            # Update config
            python3 -c "
import configparser
config = configparser.ConfigParser()
config.read('$HOME/.parallelai/config')
if not config.has_section('api_keys'):
    config.add_section('api_keys')
config.set('api_keys', 'openrouter', '$new_key')
with open('$HOME/.parallelai/config', 'w') as f:
    config.write(f)
print('✅ Key updated')
            "
            echo ""
            echo "Testing new key..."
            ./parallelai query --provider openrouter "Test with new key"
        else
            echo "❌ No key entered"
        fi
        ;;
    2)
        echo ""
        echo "Removing OpenRouter key from config..."
        python3 -c "
import configparser
config = configparser.ConfigParser()
config.read('$HOME/.parallelai/config')
if config.has_section('api_keys'):
    config.remove_option('api_keys', 'openrouter')
    with open('$HOME/.parallelai/config', 'w') as f:
        config.write(f)
print('✅ OpenRouter key removed')
        "
        echo ""
        echo "OpenRouter will be skipped until you add a new key."
        ;;
    3)
        echo "❌ Cancelled"
        ;;
    *)
        echo "❌ Invalid choice"
        ;;
esac

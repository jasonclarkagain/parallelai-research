"""
Integrated Key Manager for ParallelAI Swarm
FIXED VERSION: Config file takes priority over environment
"""
import os
import sys
import json
import configparser
from pathlib import Path
from typing import Optional, Dict, Any, List
import re

# Config paths
CONFIG_DIR = Path.home() / '.parallelai'
CONFIG_FILE = CONFIG_DIR / 'config'
HOME_DIR = Path.home()

class IntegratedKeyManager:
    """Key manager that integrates with existing swarm"""
    
    def __init__(self):
        self.config_dir = CONFIG_DIR
        self.config_file = CONFIG_FILE
        self.ensure_config_dir()
    
    def ensure_config_dir(self):
        """Ensure config directory exists"""
        self.config_dir.mkdir(exist_ok=True)
    
    def load_keys(self) -> Dict[str, str]:
        """
        Load API keys with CORRECTED priority:
        1. Config file (primary - what you set with keys setup)
        2. Environment variables (fallback)
        3. Existing orchestrator files (legacy migration)
        """
        keys = {}
        
        # 1. FIRST: Config file (this is what user explicitly sets)
        if self.config_file.exists():
            config = configparser.ConfigParser()
            config.read(self.config_file)
            
            if config.has_section('api_keys'):
                for provider, key in config.items('api_keys'):
                    if key and key.strip():  # Only add if key is not empty
                        keys[provider] = key.strip()
                        print(f"🔑 DEBUG: Loaded {provider} from config: {key[:12]}...")
        
        # 2. SECOND: Environment variables (fallback, but don't override config)
        env_keys = {
            'openai': os.getenv('OPENAI_API_KEY'),
            'anthropic': os.getenv('ANTHROPIC_API_KEY'),
            'groq': os.getenv('GROQ_API_KEY'),
            'together': os.getenv('TOGETHER_API_KEY'),
            'openrouter': os.getenv('OPENROUTER_API_KEY'),
        }
        
        for provider, key in env_keys.items():
            if key and key.strip() and provider not in keys:  # Only if not already in config
                keys[provider] = key.strip()
                print(f"🔑 DEBUG: Loaded {provider} from env: {key[:12]}...")
        
        # 3. Update environment for compatibility (but don't override existing)
        for provider, key in keys.items():
            env_var = self._provider_to_env_var(provider)
            if env_var and key and not os.getenv(env_var):
                os.environ[env_var] = key
        
        return keys
    
    def _provider_to_env_var(self, provider: str) -> Optional[str]:
        """Convert provider name to environment variable name"""
        mapping = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'groq': 'GROQ_API_KEY',
            'together': 'TOGETHER_API_KEY',
            'openrouter': 'OPENROUTER_API_KEY',
        }
        return mapping.get(provider)
    
    def save_keys(self, keys: Dict[str, str]) -> bool:
        """Save API keys to config file"""
        config = configparser.ConfigParser()
        
        if self.config_file.exists():
            config.read(self.config_file)
        
        if not config.has_section('api_keys'):
            config.add_section('api_keys')
        
        for provider, key in keys.items():
            if key:
                config.set('api_keys', provider, key)
        
        try:
            with open(self.config_file, 'w') as f:
                config.write(f)
            
            # Secure permissions
            self.config_file.chmod(0o600)
            
            return True
        except Exception as e:
            print(f"Error saving keys: {e}")
            return False
    
    def set_api_key(self, provider: str, key: str) -> bool:
        """Set a single API key"""
        # Load existing keys
        current_keys = self.load_keys()
        
        # Update the specific key
        current_keys[provider] = key
        
        # Save all keys
        return self.save_keys(current_keys)
    
    def migrate_keys(self) -> Dict[str, str]:
        """
        Migrate keys from old format to new format
        This is a stub function for compatibility
        """
        print("⚠️  Note: migrate_keys is deprecated, using integrated key system")
        return self.load_keys()
    
    def interactive_setup(self):
        """Interactive setup wizard"""
        print("\n🔐 ParallelAI API Key Setup")
        print("=" * 40)
        print("\nLet's set up your API keys.\n")
        
        providers = [
            ('openai', 'OpenAI (ChatGPT, GPT-4)', 'https://platform.openai.com/api-keys'),
            ('anthropic', 'Anthropic (Claude)', 'https://console.anthropic.com/account/keys'),
            ('groq', 'Groq (Llama 3)', 'https://console.groq.com/keys'),
            ('together', 'Together AI', 'https://api.together.xyz/settings/api-keys'),
            ('openrouter', 'OpenRouter', 'https://openrouter.ai/keys'),
        ]
        
        keys = {}
        
        for provider, description, url in providers:
            print(f"\n{description}")
            print(f"Get key from: {url}")
            response = input(f"Enter {provider} API key (or press Enter to skip): ").strip()
            
            if response:
                keys[provider] = response
                print(f"✓ {provider} key saved")
            else:
                print(f"✗ {provider} skipped")
        
        if keys:
            if self.save_keys(keys):
                print(f"\n✅ Keys saved to: {self.config_file}")
                print("🔒 File permissions set to 600 (owner read/write only)")
            else:
                print("\n❌ Failed to save keys")
        else:
            print("\n⚠️  No keys were entered")
    
    def list_keys(self, show_full: bool = False) -> Dict[str, str]:
        """List all configured keys"""
        keys = self.load_keys()
        
        if not keys:
            print("❌ No API keys configured")
            return {}
        
        print("\n🔐 Configured API Keys:")
        print("=" * 40)
        
        for provider, key in keys.items():
            if key:
                if show_full:
                    display = key
                else:
                    display = f"{key[:4]}...{key[-4:]}" if len(key) > 8 else "***"
                print(f"✅ {provider:15} {display}")
            else:
                print(f"❌ {provider:15} Not set")
        
        return keys

# Create global instance
key_manager = IntegratedKeyManager()

# Convenience functions
def load_keys() -> Dict[str, str]:
    return key_manager.load_keys()

def save_keys(keys: Dict[str, str]) -> bool:
    return key_manager.save_keys(keys)

def set_api_key(provider: str, key: str) -> bool:
    return key_manager.set_api_key(provider, key)

def migrate_keys() -> Dict[str, str]:
    """Compatibility function"""
    return key_manager.migrate_keys()

def setup_interactive():
    return key_manager.interactive_setup()

def list_keys(show_full: bool = False) -> Dict[str, str]:
    return key_manager.list_keys(show_full)

def get_key(provider: str) -> Optional[str]:
    keys = key_manager.load_keys()
    return keys.get(provider)

"""
Enhanced API Key Manager for ParallelAI
Integrates with existing orchestrator files
"""
import os
import sys
import json
import configparser
from pathlib import Path
from typing import Optional, Dict, Any, List
import click
import requests

# Add current directory to path to import existing modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

CONFIG_DIR = Path.home() / '.parallelai'
CONFIG_FILE = CONFIG_DIR / 'config'
ORCHESTRATORS_DIR = Path.home()  # Your home directory with orchestrator files

class APIKeyManager:
    """Manages API keys for ParallelAI"""
    
    def __init__(self):
        self.config_dir = CONFIG_DIR
        self.config_file = CONFIG_FILE
        self.ensure_config_dir()
    
    def ensure_config_dir(self):
        """Ensure config directory exists"""
        self.config_dir.mkdir(exist_ok=True)
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """
        Get API key with multiple fallback methods:
        1. Environment variable
        2. Config file
        3. Existing orchestrator files
        4. .api_keys directory
        """
        # 1. Environment variables
        env_map = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'groq': 'GROQ_API_KEY',
            'together': 'TOGETHER_API_KEY',
            'openrouter': 'OPENROUTER_API_KEY',
            'gemini': 'GEMINI_API_KEY',
            'mistral': 'MISTRAL_API_KEY',
            'cohere': 'COHERE_API_KEY',
            'huggingface': 'HUGGINGFACE_TOKEN'
        }
        
        env_var = env_map.get(provider)
        if env_var and os.getenv(env_var):
            return os.getenv(env_var)
        
        # 2. Config file
        if self.config_file.exists():
            config = configparser.ConfigParser()
            config.read(self.config_file)
            if config.has_section('api_keys'):
                key = config.get('api_keys', provider, fallback=None)
                if key:
                    return key
        
        # 3. Check existing orchestrator files
        key = self._find_key_in_orchestrators(provider)
        if key:
            return key
        
        # 4. Check .api_keys directory
        api_keys_dir = Path.home() / '.api_keys'
        if api_keys_dir.exists():
            key_file = api_keys_dir / f"{provider}.key"
            if key_file.exists():
                with open(key_file, 'r') as f:
                    return f.read().strip()
        
        return None
    
    def _find_key_in_orchestrators(self, provider: str) -> Optional[str]:
        """Search for API keys in existing orchestrator files"""
        # Common patterns in your existing files
        patterns = {
            'openai': [r'OPENAI_API_KEY\s*[=:]\s*["\']([^"\']+)["\']', 
                      r'sk-[a-zA-Z0-9]{48}'],
            'anthropic': [r'ANTHROPIC_API_KEY\s*[=:]\s*["\']([^"\']+)["\']',
                         r'sk-ant-[a-zA-Z0-9]{48}'],
            'groq': [r'GROQ_API_KEY\s*[=:]\s*["\']([^"\']+)["\']',
                    r'gsk_[a-zA-Z0-9]{48}'],
            'together': [r'TOGETHER_API_KEY\s*[=:]\s*["\']([^"\']+)["\']'],
            'openrouter': [r'OPENROUTER_API_KEY\s*[=:]\s*["\']([^"\']+)["\']']
        }
        
        import re
        
        # Search in common orchestrator files
        search_files = [
            'ai_orchestrator.py',
            'working_orchestrator.py',
            'ultimate_ai_system.py',
            'cloud_orchestrator.py',
            'simple_ai.py',
            '.ai_config',
            'load_ai_keys.py'
        ]
        
        for file_name in search_files:
            file_path = ORCHESTRATORS_DIR / file_name
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    # Look for patterns
                    for pattern in patterns.get(provider, []):
                        matches = re.search(pattern, content)
                        if matches:
                            # Extract the key
                            if matches.groups():
                                return matches.group(1)
                            else:
                                return matches.group(0)
                except:
                    continue
        
        return None
    
    def set_api_key(self, provider: str, key: str) -> None:
        """Set API key in config file"""
        config = configparser.ConfigParser()
        if self.config_file.exists():
            config.read(self.config_file)
        
        if not config.has_section('api_keys'):
            config.add_section('api_keys')
        
        config.set('api_keys', provider, key)
        
        with open(self.config_file, 'w') as f:
            config.write(f)
        
        # Secure permissions
        self.config_file.chmod(0o600)
        
        # Also update environment for current session
        env_map = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'groq': 'GROQ_API_KEY',
            'together': 'TOGETHER_API_KEY',
            'openrouter': 'OPENROUTER_API_KEY'
        }
        
        env_var = env_map.get(provider)
        if env_var:
            os.environ[env_var] = key
        
        return True
    
    def migrate_existing_keys(self) -> Dict[str, bool]:
        """Migrate keys from existing orchestrator files to unified config"""
        results = {}
        providers = ['openai', 'anthropic', 'groq', 'together', 'openrouter']
        
        for provider in providers:
            key = self._find_key_in_orchestrators(provider)
            if key:
                self.set_api_key(provider, key)
                results[provider] = True
            else:
                results[provider] = False
        
        return results
    
    def list_keys(self, masked: bool = True) -> Dict[str, str]:
        """List all configured API keys"""
        keys = {}
        
        if self.config_file.exists():
            config = configparser.ConfigParser()
            config.read(self.config_file)
            
            if config.has_section('api_keys'):
                for provider, key in config.items('api_keys'):
                    if masked and key:
                        if len(key) > 8:
                            keys[provider] = f"{key[:4]}...{key[-4:]}"
                        else:
                            keys[provider] = "***"
                    else:
                        keys[provider] = key
        
        return keys
    
    def test_provider(self, provider: str) -> Dict[str, Any]:
        """Test API key for a provider"""
        from parallelai.utils.providers import get_provider_client
        
        try:
            client = get_provider_client(provider)
            if client.test_connection():
                return {'valid': True, 'message': '✅ Connection successful'}
            else:
                return {'valid': False, 'message': '❌ Connection failed'}
        except Exception as e:
            return {'valid': False, 'message': f'❌ Error: {str(e)}'}
    
    def get_config(self) -> Dict[str, Any]:
        """Get all configuration"""
        config = {}
        
        if self.config_file.exists():
            parser = configparser.ConfigParser()
            parser.read(self.config_file)
            
            for section in parser.sections():
                config[section] = dict(parser.items(section))
        
        return config

# Singleton instance
key_manager = APIKeyManager()

# Convenience functions
def get_api_key(provider: str) -> Optional[str]:
    return key_manager.get_api_key(provider)

def set_api_key(provider: str, key: str) -> None:
    return key_manager.set_api_key(provider, key)

def list_keys(masked: bool = True) -> Dict[str, str]:
    return key_manager.list_keys(masked)

def test_key(provider: str) -> Dict[str, Any]:
    return key_manager.test_provider(provider)

def migrate_keys() -> Dict[str, bool]:
    return key_manager.migrate_existing_keys()

def get_config() -> Dict[str, Any]:
    return key_manager.get_config()

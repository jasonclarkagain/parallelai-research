"""
Provider clients that integrate with existing orchestrators
"""
import os
import json
import requests
from typing import Optional, Dict, Any, List
from pathlib import Path

# Try to import your existing orchestrator modules
try:
    # These are your existing files
    sys.path.insert(0, str(Path.home()))
    import ai_orchestrator as existing_ai
    HAS_EXISTING_AI = True
except ImportError:
    HAS_EXISTING_AI = False

class BaseProvider:
    """Base class for all LLM providers"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = None
        self.name = "base"
    
    def test_connection(self) -> bool:
        """Test if API key is valid"""
        raise NotImplementedError
    
    def query(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Query the provider"""
        raise NotImplementedError
    
    def get_models(self) -> List[str]:
        """Get available models"""
        raise NotImplementedError

class OpenAIProvider(BaseProvider):
    """OpenAI API provider"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key or os.getenv('OPENAI_API_KEY'))
        self.base_url = "https://api.openai.com/v1"
        self.name = "openai"
    
    def test_connection(self) -> bool:
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(f"{self.base_url}/models", 
                                  headers=headers, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def query(self, prompt: str, **kwargs) -> Dict[str, Any]:
        # Try to use existing orchestrator if available
        if HAS_EXISTING_AI and hasattr(existing_ai, 'query_openai'):
            try:
                return existing_ai.query_openai(prompt, **kwargs)
            except:
                pass
        
        # Fallback to direct API call
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": kwargs.get('model', 'gpt-3.5-turbo'),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get('temperature', 0.7),
            "max_tokens": kwargs.get('max_tokens', 1000)
        }
        
        response = requests.post(f"{self.base_url}/chat/completions",
                               headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return {
                'success': True,
                'content': result['choices'][0]['message']['content'],
                'model': result['model'],
                'usage': result.get('usage', {})
            }
        else:
            return {
                'success': False,
                'error': f"API error: {response.status_code}",
                'details': response.text
            }

class GroqProvider(BaseProvider):
    """Groq API provider"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key or os.getenv('GROQ_API_KEY'))
        self.base_url = "https://api.groq.com/openai/v1"
        self.name = "groq"
    
    def test_connection(self) -> bool:
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(f"{self.base_url}/models",
                                  headers=headers, timeout=10)
            return response.status_code == 200
        except:
            return False

# Add other providers similarly...
class TogetherAIProvider(BaseProvider):
    """Together AI provider"""
    pass

class OpenRouterProvider(BaseProvider):
    """OpenRouter provider"""
    pass

# Provider factory
def get_provider_client(provider_name: str, api_key: Optional[str] = None):
    """Get provider client instance"""
    providers = {
        'openai': OpenAIProvider,
        'groq': GroqProvider,
        'together': TogetherAIProvider,
        'openrouter': OpenRouterProvider,
        # Add more...
    }
    
    provider_class = providers.get(provider_name.lower())
    if not provider_class:
        raise ValueError(f"Unknown provider: {provider_name}")
    
    return provider_class(api_key)

def get_all_providers() -> Dict[str, BaseProvider]:
    """Get all configured providers"""
    from .key_manager import get_api_key
    
    providers = {}
    for provider_name in ['openai', 'groq', 'together', 'openrouter']:
        api_key = get_api_key(provider_name)
        if api_key:
            providers[provider_name] = get_provider_client(provider_name, api_key)
    
    return providers

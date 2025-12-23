"""
Configuration for ParallelAI Swarm
"""
API_ENDPOINTS = {
    "openai": "https://api.openai.com/v1/chat/completions",
    "anthropic": "https://api.anthropic.com/v1/messages",
    "groq": "https://api.groq.com/openai/v1/chat/completions",
    "together": "https://api.together.xyz/v1/chat/completions",
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
}

# Default models - let's try different OpenRouter models
DEFAULT_MODELS = {
    "openai": "gpt-3.5-turbo",
    "anthropic": "claude-3-haiku-20240307",
    "groq": "llama-3.1-8b-instant",
    "together": "meta-llama/Llama-3-70b-chat-hf",
    # Try different OpenRouter models
    "openrouter": "google/gemini-3-flash-preview",  # Free model
}

def get_headers(provider: str, api_key: str) -> dict:
    """Get headers for API requests"""
    base_headers = {"Content-Type": "application/json"}
    
    if not api_key:
        return base_headers
    
    if provider == "openai":
        return {**base_headers, "Authorization": f"Bearer {api_key}"}
    
    elif provider == "anthropic":
        return {
            **base_headers,
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        }
    
    elif provider == "groq":
        return {**base_headers, "Authorization": f"Bearer {api_key}"}
    
    elif provider == "together":
        return {**base_headers, "Authorization": f"Bearer {api_key}"}
    
    elif provider == "openrouter":
        return {
            **base_headers,
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://github.com/parallelai-research/parallelai",
            "X-Title": "ParallelAI Research"
        }
    
    return base_headers

# For backward compatibility
API_KEYS = {}
HEADERS = {}

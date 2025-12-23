"""
Configuration for ParallelAI - Free Models Only
"""
API_ENDPOINTS = {
    "anthropic": "https://api.anthropic.com/v1/messages",
    "groq": "https://api.groq.com/openai/v1/chat/completions",
    "together": "https://api.together.xyz/v1/chat/completions",
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
}

# Only free/cheap models
DEFAULT_MODELS = {
    "anthropic": "claude-3-haiku-20240307",  # Claude's cheapest
    "groq": "llama-3.1-8b-instant",  # Free tier
    "together": "meta-llama/Llama-3-70b-chat-hf",  # Free credits
    "openrouter": "google/gemini-3-flash-preview",  # Free preview
}

def get_headers(provider: str, api_key: str) -> dict:
    base_headers = {"Content-Type": "application/json"}
    
    if not api_key:
        return base_headers
    
    if provider == "anthropic":
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

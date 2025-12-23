#!/usr/bin/env python3
"""
ParallelAI API Client - For connecting other apps to your ParallelAI platform
"""
import requests
import json
from typing import Dict, List, Optional, Union
import warnings

class ParallelAIClient:
    """Client for ParallelAI API Server"""
    
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}"
            })
    
    def set_api_key(self, api_key: str):
        """Set or update the API key"""
        self.api_key = api_key
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}"
        })
    
    def get_status(self) -> Dict:
        """Get API server status"""
        response = self.session.get(f"{self.base_url}/status")
        response.raise_for_status()
        return response.json()
    
    def list_providers(self) -> Dict:
        """List available AI providers"""
        response = self.session.get(f"{self.base_url}/providers")
        response.raise_for_status()
        return response.json()
    
    def query(
        self, 
        query: str, 
        provider: Optional[str] = None,
        timeout: int = 30
    ) -> Dict:
        """
        Query AI providers
        
        Args:
            query: The question or prompt to send
            provider: Specific provider to use (optional, queries all if None)
            timeout: Request timeout in seconds
        
        Returns:
            Dictionary with query results
        """
        params = {"query": query}
        if provider:
            params["provider"] = provider
        
        response = self.session.post(
            f"{self.base_url}/query",
            params=params,
            timeout=timeout
        )
        response.raise_for_status()
        return response.json()
    
    def query_single(self, query: str, provider: str) -> str:
        """
        Query a single provider and return just the response text
        
        Args:
            query: The question or prompt
            provider: Provider to use (e.g., 'groq', 'anthropic')
        
        Returns:
            Response text from the provider
        """
        result = self.query(query, provider)
        
        if result.get("success"):
            return result.get("response", "")
        else:
            error = result.get("error", "Unknown error")
            raise Exception(f"{provider} error: {error}")
    
    def compare_providers(self, query: str) -> Dict[str, str]:
        """
        Query all providers and compare responses
        
        Args:
            query: The question to send to all providers
        
        Returns:
            Dictionary mapping provider names to their responses
        """
        result = self.query(query)
        
        if result.get("success"):
            responses = {}
            for provider, data in result.get("results", {}).items():
                if data.get("success"):
                    responses[provider] = data.get("response", "")
                else:
                    responses[provider] = f"Error: {data.get('error', 'Unknown')}"
            return responses
        else:
            raise Exception(f"Query failed: {result.get('error', 'Unknown')}")
    
    def health_check(self) -> bool:
        """Check if API server is healthy"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

# Convenience functions for quick use
def create_client(api_key: str, base_url: str = "http://localhost:8000") -> ParallelAIClient:
    """Create a new ParallelAI client instance"""
    return ParallelAIClient(base_url=base_url, api_key=api_key)

def quick_query(api_key: str, query: str, provider: str = None) -> Dict:
    """Quick one-off query"""
    client = ParallelAIClient(api_key=api_key)
    return client.query(query, provider)

# Example usage
if __name__ == "__main__":
    # Example 1: Using the client
    print("Example 1: Basic usage")
    print("-" * 50)
    
    # Replace with your actual API key
    API_KEY = "pai_your_generated_api_key_here"
    
    client = ParallelAIClient(api_key=API_KEY)
    
    # Check status
    status = client.get_status()
    print(f"API Status: {status.get('status')}")
    
    # List providers
    providers = client.list_providers()
    print(f"Available providers: {len(providers.get('providers', []))}")
    
    # Query a specific provider
    print("\nQuerying Groq...")
    try:
        result = client.query("What is the capital of France?", provider="groq")
        if result.get("success"):
            print(f"Response: {result.get('response', '')[:100]}...")
        else:
            print(f"Error: {result.get('error')}")
    except Exception as e:
        print(f"Query failed: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Client library ready!")
    print("\nUsage in your other apps:")
    print('''
    from parallelai_client import ParallelAIClient
    
    # Initialize client
    client = ParallelAIClient(
        base_url="http://localhost:8000",
        api_key="your_api_key_here"
    )
    
    # Make queries
    response = client.query("Your question here", provider="groq")
    print(response.get("response"))
    ''')

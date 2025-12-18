#!/bin/bash
echo "🚀 Installing ParallelAI CLI"
echo "============================="

# 1. Make sure we're in the right directory
cd ~/projects/parallelai

# 2. Make the CLI globally accessible
sudo cp parallelai-cli-fixed /usr/local/bin/parallelai
sudo chmod +x /usr/local/bin/parallelai

# 3. Create a more robust CLI with better error handling
cat > ~/projects/parallelai/parallelai-v2 << 'EOF2'
#!/usr/bin/env python3
import os
import sys
import asyncio
import aiohttp
import json
from typing import Dict, List, Optional

class ParallelAI:
    """Enhanced Parallel AI Client with fallback and retry logic"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.setup_providers()
        
    def setup_providers(self):
        """Configure AI providers with priority order"""
        self.providers = [
            {
                'name': 'groq',
                'url': 'https://api.groq.com/openai/v1/chat/completions',
                'key': os.getenv('GROQ_API_KEY'),
                'model': 'llama-3.3-70b-versatile',
                'priority': 1,
                'headers': lambda key: {
                    'Authorization': f'Bearer {key}',
                    'Content-Type': 'application/json'
                }
            },
            {
                'name': 'together',
                'url': 'https://api.together.xyz/v1/chat/completions',
                'key': os.getenv('TOGETHER_API_KEY'),
                'model': 'mistralai/Mixtral-8x7B-Instruct-v0.1',
                'priority': 2,
                'headers': lambda key: {
                    'Authorization': f'Bearer {key}',
                    'Content-Type': 'application/json'
                }
            },
            {
                'name': 'openrouter',
                'url': 'https://openrouter.ai/api/v1/chat/completions',
                'key': os.getenv('OPENROUTER_API_KEY'),
                'model': 'mistralai/mistral-7b-instruct:free',
                'priority': 3,
                'headers': lambda key: {
                    'Authorization': f'Bearer {key}',
                    'HTTP-Referer': 'https://parallelai.com',
                    'X-Title': 'ParallelAI Security Tool',
                    'Content-Type': 'application/json'
                }
            }
        ]
        # Sort by priority
        self.providers.sort(key=lambda x: x['priority'])
    
    async def query_with_fallback(self, prompt: str, max_tokens: int = 300) -> Dict:
        """Query providers with fallback strategy"""
        tasks = []
        
        for provider in self.providers:
            if provider['key'] and len(provider['key']) > 20:
                tasks.append(self._query_single(provider, prompt, max_tokens))
        
        # Try providers in parallel, return first successful response
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        
        for task in done:
            result = task.result()
            if result['success']:
                # Cancel pending tasks
                for pending_task in pending:
                    pending_task.cancel()
                return result
        
        # If no success, return all errors
        all_results = []
        for task in tasks:
            if task.done():
                all_results.append(task.result())
        
        return {
            'success': False,
            'error': 'All providers failed',
            'details': all_results
        }
    
    async def query_all(self, prompt: str, max_tokens: int = 300) -> Dict:
        """Query all providers and compile results"""
        tasks = []
        
        for provider in self.providers:
            if provider['key'] and len(provider['key']) > 20:
                tasks.append(self._query_single(provider, prompt, max_tokens))
        
        if not tasks:
            return {"error": "No valid API keys configured"}
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        compiled = {}
        for i, result in enumerate(results):
            provider = self.providers[i]['name']
            if isinstance(result, Exception):
                compiled[provider] = {'success': False, 'error': str(result)}
            else:
                compiled[provider] = result
        
        return compiled
    
    async def _query_single(self, provider: Dict, prompt: str, max_tokens: int) -> Dict:
        """Query a single provider"""
        name = provider['name']
        headers = provider['headers'](provider['key'])
        payload = {
            'model': provider['model'],
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': max_tokens,
            'temperature': 0.7
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    provider['url'],
                    json=payload,
                    headers=headers
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        content = data.get('choices', [{}])[0].get('message', {}).get('content', 'No content')
                        return {
                            'success': True, 
                            'provider': name,
                            'response': content,
                            'model': provider['model']
                        }
                    else:
                        error_text = await response.text()
                        return {
                            'success': False,
                            'provider': name,
                            'error': f'HTTP {response.status}',
                            'details': error_text[:200]
                        }
                        
        except asyncio.TimeoutError:
            return {'success': False, 'provider': name, 'error': 'Timeout'}
        except Exception as e:
            return {'success': False, 'provider': name, 'error': f'Connection: {str(e)}'}

def print_help():
    """Print help information"""
    print("""
ParallelAI CLI - Multi-Provider AI Assistant
============================================

Usage:
  parallelai "Your query here"              # Fast response (first provider)
  parallelai --all "Your query here"       # Get all provider responses
  parallelai --help                        # Show this help

Examples:
  parallelai "Explain quantum computing"
  parallelai --all "Write a Python function to reverse a string"
  parallelai "What are best practices for API security?"

Environment Variables (set in ~/projects/parallelai/.env):
  GROQ_API_KEY=your_groq_key_here
  TOGETHER_API_KEY=your_together_key_here
  OPENROUTER_API_KEY=your_openrouter_key_here
""")

async def main():
    if len(sys.argv) < 2 or '--help' in sys.argv or '-h' in sys.argv:
        print_help()
        sys.exit(0)
    
    mode = 'all' if '--all' in sys.argv else 'fast'
    
    # Extract query (remove mode flags)
    query_parts = []
    for arg in sys.argv[1:]:
        if arg not in ['--all', '--fast']:
            query_parts.append(arg)
    
    query = " ".join(query_parts)
    
    if not query:
        print("Error: No query provided")
        print_help()
        sys.exit(1)
    
    print(f"🔍 Query: {query}")
    
    client = ParallelAI()
    
    if mode == 'fast':
        print("⚡ Fast mode (first successful response)...\n")
        result = await client.query_with_fallback(query)
        
        if result['success']:
            print(f"✅ {result['provider'].upper()} ({result['model']}):")
            print(f"{result['response']}")
            print(f"\n📊 Provider: {result['provider']}")
        else:
            print("❌ All providers failed:")
            for detail in result.get('details', []):
                print(f"   • {detail.get('provider')}: {detail.get('error')}")
    
    else:  # all mode
        print("🔄 Querying all providers...\n")
        results = await client.query_all(query)
        
        print("=" * 60)
        for provider, result in results.items():
            if result.get('success'):
                response = result['response']
                model = result.get('model', 'N/A')
                print(f"✅ {provider.upper()} ({model}):")
                print(f"{response[:500]}..." if len(response) > 500 else response)
            else:
                print(f"❌ {provider.upper()}: {result.get('error', 'Unknown')}")
                if 'details' in result:
                    print(f"   Details: {result['details'][:100]}")
            print("-" * 40)
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
EOF2

chmod +x ~/projects/parallelai/parallelai-v2
sudo cp ~/projects/parallelai/parallelai-v2 /usr/local/bin/parallelai2

echo ""
echo "✅ Installation complete!"
echo ""
echo "📦 Installed commands:"
echo "   • parallelai    - Fast mode (uses first working provider)"
echo "   • parallelai2   - Enhanced version with --all flag"
echo ""
echo "📝 Examples:"
echo "   parallelai \"Explain blockchain technology\""
echo "   parallelai2 --all \"Compare Python vs JavaScript\""
echo ""
echo "🔧 To update your PATH permanently, add to ~/.bashrc:"
echo "   export PATH=\$PATH:/usr/local/bin"

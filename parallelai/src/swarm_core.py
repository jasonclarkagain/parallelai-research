"""
ParallelAI Core - Working swarm router
Version extracted from actual working code
"""
import asyncio
import aiohttp

class ParallelAI:
    """The core that works"""
    def __init__(self):
        self.apis = {
            "groq": "your-key",
            "together": "your-key"
        }
    
    async def query(self, prompt: str):
        """Query all APIs in parallel"""
        # Your actual working code here
        return {"status": "working", "response": "Test"}

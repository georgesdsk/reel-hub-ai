from groq import AsyncGroq
import json

class CategorizerAdapter:
    def __init__(self, api_key):
        self.client = AsyncGroq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
    async def categorize(self, transcript, title=None, language="es"):
        try:
            # Placeholder for actual Groq call to be fast
            return {"category": "otros", "tags": ["video"], "ingredients": [], "steps": []}
        except:
            return {"category": "otros", "tags": [], "ingredients": [], "steps": []}

import os
from crewai.tools import BaseTool
from tavily import TavilyClient

class TavilySearchTool(BaseTool):
    name: str = "Tavily Web Search"
    description: str = "Search the web for startup info, funding news, and market trends."

    class Config:
        arbitrary_types_allowed = True

    def _run(self, query: str) -> str:
        try:
            client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
            response = client.search(
                query=query,
                search_depth="advanced",
                max_results=6,
                include_answer=True,
            )
            results = []
            if response.get("answer"):
                results.append(f"Summary: {response['answer']}\n")
            for r in response.get("results", []):
                results.append(
                    f"Title: {r.get('title')}\n"
                    f"URL: {r.get('url')}\n"
                    f"Content: {r.get('content','')[:400]}\n---"
                )
            return "\n".join(results) or "No results found."
        except Exception as e:
            return f"Search error: {str(e)}"
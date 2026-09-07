"""External knowledge retrieval used by FLARE."""

from __future__ import annotations

from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class RetrievedDocument:
    title: str
    text: str
    url: str


class WikipediaRetriever:
    """Retrieve short article introductions from a Wikipedia language edition."""

    def __init__(self, language: str = "ko", timeout: float = 10.0) -> None:
        self.endpoint = f"https://{language}.wikipedia.org/w/api.php"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "educational-flare-rag/0.1"

    def search(self, query: str, limit: int = 3) -> list[RetrievedDocument]:
        response = self.session.get(
            self.endpoint,
            params={
                "action": "query",
                "generator": "search",
                "gsrsearch": query,
                "gsrlimit": limit,
                "prop": "extracts|info",
                "exintro": 1,
                "explaintext": 1,
                "inprop": "url",
                "format": "json",
                "formatversion": 2,
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        pages = response.json().get("query", {}).get("pages", [])
        return [
            RetrievedDocument(
                title=page.get("title", ""),
                text=page.get("extract", "").strip(),
                url=page.get("fullurl", ""),
            )
            for page in pages
            if page.get("extract")
        ]

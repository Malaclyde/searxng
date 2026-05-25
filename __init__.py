"""SearXNG search plugin for Hermes Agent."""
import json
import logging
import os

logger = logging.getLogger(__name__)


def register(ctx):
    SEARXNG_SEARCH = {
        "name": "searxng_search",
        "description": (
            "Search the web using a self-hosted SearXNG metasearch instance. "
            "Supports category filtering, engine selection, time range, and language. "
            "Free, private, no API key needed."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query. Supports operators like site:github.com, filetype:pdf, etc.",
                },
                "categories": {
                    "type": "string",
                    "description": "Comma-separated categories: general, images, videos, news, it, science, files, social media, music",
                },
                "engines": {
                    "type": "string",
                    "description": "Comma-separated engine names (e.g. google,duckduckgo,github,stackoverflow,reddit)",
                },
                "time_range": {
                    "type": "string",
                    "enum": ["", "day", "month", "year"],
                    "description": "Time range filter",
                },
                "language": {
                    "type": "string",
                    "description": "Language code (e.g. en, de, fr)",
                },
                "limit": {
                    "type": "integer",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 50,
                    "description": "Maximum number of results to return",
                },
            },
            "required": ["query"],
        },
    }

    ctx.register_tool(
        name="searxng_search",
        toolset="searxng",
        schema=SEARXNG_SEARCH,
        handler=handle_searxng_search,
    )


def handle_searxng_search(params, **kwargs):
    import httpx

    query = params.get("query", "")
    base_url = os.environ.get("SEARXNG_URL", "http://localhost:9000")

    search_params = {
        "q": query,
        "format": "json",
        "safesearch": "0",
    }

    categories = params.get("categories")
    if categories:
        search_params["categories"] = categories

    engines = params.get("engines")
    if engines:
        search_params["engines"] = engines

    time_range = params.get("time_range")
    if time_range:
        search_params["time_range"] = time_range

    language = params.get("language")
    if language:
        search_params["language"] = language

    limit = params.get("limit", 10)

    try:
        response = httpx.get(
            f"{base_url}/search",
            params=search_params,
            headers={"User-Agent": "hermes-searxng/1.0"},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        limited = results[:limit]

        lines = []

        answers = data.get("answers", [])
        if answers:
            lines.append("## Answers")
            for a in answers:
                lines.append(f"- {a}")
            lines.append("")

        infoboxes = data.get("infoboxes", [])
        if infoboxes:
            lines.append("## Infobox")
            for box in infoboxes:
                lines.append(f"**{box.get('infobox', '')}**")
                for attr in box.get("attributes", []):
                    lines.append(f"  {attr.get('label', '')}: {attr.get('value', '')}")
            lines.append("")

        if not limited:
            lines.append("No results found.")
        else:
            for i, r in enumerate(limited, 1):
                title = r.get("title", "")
                url = r.get("url", "")
                snippet = r.get("content", "")
                engine = r.get("engine", "")
                published = r.get("publishedDate", "")
                lines.append(f"{i}. **{title}**")
                lines.append(f"   URL: {url}")
                if snippet:
                    lines.append(f"   {snippet}")
                meta = []
                if engine:
                    meta.append(f"via {engine}")
                if published:
                    meta.append(published)
                if meta:
                    lines.append(f"   ({', '.join(meta)})")
                lines.append("")

        suggestions = data.get("suggestions", [])
        if suggestions:
            lines.append("## Suggestions")
            for s in suggestions:
                lines.append(f"- {s}")

        correction = data.get("correction", "")
        if correction:
            lines.append(f"**Did you mean:** {correction}")

        unresponsive = data.get("unresponsive_engines", [])
        if unresponsive:
            lines.append(f"\n*Note: {len(unresponsive)} engine(s) did not respond*")

        return json.dumps({"success": True, "data": "\n".join(lines)})

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 403:
            return json.dumps({
                "error": "SearXNG returned 403. JSON format may be disabled. "
                         "Enable it by adding 'json' to the formats list in settings.yml.",
            })
        return json.dumps({"error": f"HTTP error: {e}"})
    except httpx.ConnectError:
        return json.dumps({
            "error": f"Cannot connect to SearXNG at {base_url}. Is the container running?",
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

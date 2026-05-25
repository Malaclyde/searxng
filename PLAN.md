# SearXNG Hermes Plugin — Implementation Plan

## Overview
Add a Hermes plugin to the root of this repo. The plugin wraps the SearXNG JSON API into a single `searxng_search` tool with full parameter support.

## Files to Create

### 1. `plugin.yaml`
```yaml
name: searxng
version: "1.0.0"
description: SearXNG metasearch — privacy-respecting web, news, image, and code search
requires_env: [SEARXNG_URL]
```

### 2. `__init__.py`
```python
def register(ctx):
    ctx.register_tool(
        name="searxng_search",
        toolset="searxng",
        schema=SEARXNG_SEARCH,
        handler=searxng_search_handler,
    )
```

### 3. Tool Schema
Parameters for `searxng_search`:
- `query` (required string)
- `categories` (optional string, e.g. "general,it,science")
- `engines` (optional string, e.g. "google,duckduckgo,github")
- `time_range` (optional enum: "day", "month", "year")
- `language` (optional string, e.g. "en")
- `limit` (optional integer, default 10)

### 4. Handler Logic
1. Read `SEARXNG_URL` from env (default `http://localhost:9000`)
2. Build query params: `q`, `format=json`, `categories`, `engines`, `time_range`, `language`, `pageno=1`, `safesearch=0`
3. `httpx.get(url, params=params, timeout=30)`
4. Format results: answers, infoboxes, results list, suggestions, unresponsive engines warning
5. Error handling: connection errors, 403 (JSON disabled), generic HTTP errors

### 5. README Update
Add "Hermes Plugin" section with install, config, and usage docs.

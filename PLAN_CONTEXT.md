# Plan: SearXNG Hermes Plugin

## Goal
Add a Hermes plugin to this repo at the root level, making it installable via `hermes plugins install Malaclyde/searxng`.

## Current State
- Root has: `opencode/searxng.ts` (OpenCode TypeScript tool)
- The TypeScript tool wraps SearXNG JSON API with full parameter support

## What Needs to Happen

### Step 1: Create Hermes plugin at root
Files to create:
- `plugin.yaml` — manifest (name: searxng)
- `__init__.py` — plugin registration code

### Step 2: Register Hermes tools
Port the SearXNG API wrapper from TypeScript to Python. The plugin should register this tool via `ctx.register_tool()`:

1. **`searxng_search`** — Full SearXNG search with parameter control
   - Parameters: `query` (required), `categories` (optional string, e.g. "general,it,science"), `engines` (optional string, e.g. "google,duckduckgo,github"), `time_range` (optional, "day"|"month"|"year"), `language` (optional, e.g. "en"), `limit` (optional int, default 10)
   - Calls: `curl -s 'http://localhost:9000/search?q=...&format=json&categories=...'` or Python httpx
   - Toolset: `searxng`

### Step 3: Update README
- Document the Hermes plugin

## SearXNG API
- Base URL: http://localhost:9000 (from SEARXNG_URL env var, fallback to localhost:9000)
- Endpoint: `/search?q={query}&format=json`
- Additional params: `categories`, `engines`, `time_range`, `language`, `pageno`
- Reference TypeScript implementation: `opencode/searxng.ts`

## References
- Hermes plugin system: https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
- Build a Hermes plugin: https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin
- SearXNG API docs: https://docs.searxng.org/dev/search_api.html
- Reference TS implementation: opencode/searxng.ts

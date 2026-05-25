# SearXNG Tools

SearXNG metasearch tools for OpenCode and Hermes Agent.

## Structure

- `opencode/searxng.ts` — OpenCode tool (TypeScript)
- `plugin.yaml` + `__init__.py` — Hermes plugin (root)

## Hermes Plugin

Install:
```bash
hermes plugins install Malaclyde/searxng
```

Or manually:
```bash
cp -r searxng ~/.hermes/plugins/searxng
```

### Configuration

Set `SEARXNG_URL` env var (default: `http://localhost:9000`).

### Tool: `searxng_search`

Parameters:
- `query` (required) — search query, supports `site:`, `filetype:`, etc.
- `categories` — comma-separated (general, images, videos, news, it, science, files)
- `engines` — comma-separated (google, duckduckgo, github, stackoverflow, reddit, etc.)
- `time_range` — day, month, or year
- `language` — language code (en, de, fr, etc.)
- `limit` — max results (default 10, max 50)

## OpenCode Tool

Copy the tool definition:
```bash
cp opencode/searxng.ts ~/.config/opencode/tools/
```

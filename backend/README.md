# Streber — MCP Server

FastAPI + pgvector RAG over pathology books (llama-index), exposed as MCP tools.

---

## English

### Run

From the repo root (`streber/`):

```bash
docker compose up -d --build
```

- `-d` — run in background. `--build` — rebuild the image first (needed after code changes).

App: `http://localhost:8000` · MCP endpoint: `http://localhost:8000/mcp`

### MCP tools

| Tool | What it does |
|---|---|
| `search_books(question, top_k=10)` | Searches the books, returns text chunks with source file and score |
| `ask_question(question)` | Answers using LLM over the found chunks |
| `list_books()` | Lists book names in `data/book` |

### Connect an MCP client

Any MCP client (Claude Code, Cursor, Claude Desktop) discovers tools via
`initialize → tools/list → tools/call` on the streamable HTTP endpoint.

```json
{
  "mcpServers": {
    "streber": {
      "type": "streamable-http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

Raw HTTP: POST to `/mcp`, use the `Mcp-Session-Id` header from the `initialize` response (`curl -L` because of the `/mcp` → `/mcp/` redirect).

### Config

`.env` in this folder: `DEEPSEEK_API_KEY`, `TYPESAFE_API_KEY`, `OPEN_API_KEY`,
`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`.

- `enable_mcp` (default `true`) — kill switch; set to `false` to disable `/mcp`.
- `mcp_path` (default `/mcp`).
- No auth yet — the port is bound to localhost only.

### Tests

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/ -v
```

Unit test for `retrieve()` (all external boundaries mocked, no database needed)
+ tool registration test.



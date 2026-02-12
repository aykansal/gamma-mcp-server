## Gamma FastMCP Server

This is a Python FastAPI + FastMCP server that wraps the Gamma APIs and exposes
an MCP HTTP endpoint that MCP Clients can connect to.

### What this server provides

- MCP tools:
  - `generate_presentation`
  - `create_from_template`
  - `get_generation_status`
  - `list_themes`
  - `list_folders`
- Health endpoint: `/health`
- MCP transport: `streamable-http` (default)
- No OAuth flow required for MCP Client (server uses `GAMMA_API_KEY` from env)
- Tool definitions live in `lib/tool.py` and are registered from `main.py`

It uses Gamma's current flows:

1. `POST /v1.0/generations` to create a generation job
2. `POST /v1.0/generations/from-template` for template-based creation
3. Poll `GET /v1.0/generations/{generationId}` until status is `completed`
4. Use `GET /v1.0/themes` and `GET /v1.0/folders` with pagination when needed

Reference: [Gamma Generate API parameters explained](https://developers.gamma.app/docs/generate-api-parameters-explained)

### 1) Setup (uv)

From `gamma-mcp/`:

```bash
uv sync
```

Create `.env` from `.env.example` and set your key:

```env
GAMMA_API_KEY=sk-gamma-...
PORT=8000
MCP_TRANSPORT=streamable-http
```

### 2) Run server

```bash
uv run python main.py
```

Server will start on:

- `http://localhost:8000/mcp` (MCP endpoint for MCP Client)
- `http://localhost:8000/health` (health check)

### 3) Add in MCP Client connector UI

In MCP Client `Add Connector` -> `Add MCP Server`:

- **Name:** `Gamma MCP`
- **URL:** `http://localhost:8000/mcp`
- **Transport:** `http`
- **Auth headers:** leave empty (Gamma key is handled server-side via env)

Then click **Discover Tools**, select `generate_presentation`, and save.

### 4) Example prompt in MCP Client

"Use Gamma MCP to generate a 10-card presentation on AI agents for product teams."
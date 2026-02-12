import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP

from lib.tool import register_tools

load_dotenv()

DEFAULT_CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

server = FastMCP(name="gamma")
REGISTERED_TOOLS = register_tools(server)


def create_app() -> FastAPI:
    mcp_app = server.http_app(path="/", transport="streamable-http")

    app = FastAPI(
        title="Gamma MCP Server",
        description="FastAPI + FastMCP server for Gamma Generate APIs (no OAuth required).",
        version="1.0.0",
        lifespan=mcp_app.lifespan,
    )

    cors_origins = [
        origin.strip() for origin in DEFAULT_CORS_ORIGINS.split(",") if origin.strip()
    ]
    if cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.get("/")
    async def root() -> dict[str, object]:
        return {
            "service": "gamma-mcp",
            "status": "ok",
            "mcp_endpoint": "/mcp",
            "auth_mode": "api-key-env-only",
            "tools": REGISTERED_TOOLS,
        }

    @app.get("/health")
    async def api_health() -> dict[str, object]:
        return {"status": "ok", "service": "gamma-mcp", "tool_count": len(REGISTERED_TOOLS)}

    app.mount("/mcp", mcp_app)
    return app


app = create_app()


def main() -> None:
    transport = os.getenv("MCP_TRANSPORT", "streamable-http").strip().lower()
    if transport == "stdio":
        server.run()
        return

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()

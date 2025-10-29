# Agent Instructions

## User Preferences

- [2024-12-19 19:15] User prefers running the app with auto-reload (reload mode) always enabled (auto_reload = true).
- [2024-12-19 19:15] User prefers that when starting the app server, it should use a random port instead of defaulting to port 8000.

## Dependencies

- [2024-12-19 18:45] This project uses FastMCP (not standard MCP library) with Pydantic for the MCP server implementation. FastMCP provides cleaner decorator-based API with @mcp.tool, @mcp.prompt, and @mcp.resource decorators.
- [2024-12-19 19:15] Pydantic v3 is not available in conda-forge channel - only Pydantic v2.x is available. FastMCP 2.0.0 works with Pydantic v2.
- [2024-12-19 19:15] FastMCP 2.10.6+ has a bug where it tries to define Pydantic fields with both `default` and `default_factory`, causing TypeError. Use FastMCP 2.0.0 instead.

## Development Workflow

- [2024-12-19 18:45] This project uses pixi for dependency management and running commands. Always use `pixi run` prefix for commands (e.g., `pixi run start-mcp-server`).

## Project Structure

- [2024-12-19 18:45] The main server implementation is in `ericmjl_productivity_mcp/server.py` using FastMCP decorators for prompts, tools, and resources.

## FastMCP Version Compatibility

- [2024-12-19 18:45] This project uses FastMCP 2.0.0 specifically. Newer versions (2.10.6+) have Pydantic compatibility issues. FastMCP 2.0.0 requires decorators to be called with parentheses: `@mcp.tool()`, `@mcp.prompt()`, `@mcp.resource()`.

## Code Patterns

- [2024-12-19 19:15] FastMCP 2.0.0 requires decorators to be called with parentheses: `@mcp.tool()`, `@mcp.prompt()`, `@mcp.resource()` instead of `@mcp.tool`, `@mcp.prompt`, `@mcp.resource`.
- [2024-12-19 19:15] FastMCP handles event loops internally - use `mcp.run()` directly instead of `asyncio.run()` to avoid "Already running asyncio in this thread" errors.
- [2024-12-19 19:15] When debugging dependency issues, check actual error messages rather than assuming compatibility problems. The FastMCP error was a bug in the library, not a Pydantic version issue.

## Server Implementation

- [2024-12-19 18:45] FastMCP handles the event loop internally, so use `mcp.run()` directly instead of `asyncio.run()`. The server runs in stdio mode by default.
- [2024-12-19 19:15] The `/remember` prompt is implemented and functional - it instructs AI agents to capture learnings from conversations and organize them in AGENTS.md with timestamped entries.

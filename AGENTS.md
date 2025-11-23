# Agent Instructions

## User Preferences

- User prefers running the app with auto-reload (reload mode) always enabled
  (auto_reload = true).
- User prefers that when starting the app server, it should use a random port
  instead of defaulting to port 8000.

## Dependencies

- This project uses FastMCP (not standard MCP library) with Pydantic for the
  MCP server implementation. FastMCP provides cleaner decorator-based API with
  @mcp.tool, @mcp.prompt, and @mcp.resource decorators.
- Pydantic v3 is not available in conda-forge channel - only Pydantic v2.x is
  available. FastMCP 2.0.0 works with Pydantic v2.
- FastMCP 2.10.6+ has a bug where it tries to define Pydantic fields with both
  `default` and `default_factory`, causing TypeError. Use FastMCP 2.0.0 instead.

## Development Workflow

- This project uses pixi for dependency management and running commands. Always
  use `pixi run` prefix for commands (e.g., `pixi run start-mcp-server`).
- **Markdownlint Rules**: Always run markdownlint on any markdown files that
  are edited or created. This ensures consistent formatting and catches common
  markdown issues. The workflow is:
  1. After editing any markdown file (`.md`), run `markdownlint <file-path>` to
     check for issues.
  2. If markdownlint is not found on PATH, install it using
     `pixi global install markdownlint-cli`. This installs it globally via pixi
     and makes it available on PATH.
  3. Always fix any issues that markdownlint raises before considering the task
     complete. Common issues include: trailing whitespace, missing blank lines
     around headers, improper list formatting, and line length violations.
  4. For multiple files, you can run `markdownlint "**/*.md"` to check all
     markdown files in the project, or specify individual files.
  5. If markdownlint reports errors, fix them immediately and re-run
     markdownlint to verify the fixes.

## Project Structure

- The main server implementation is in `ericmjl_productivity_mcp/server.py`
  using FastMCP decorators for prompts, tools, and resources.

## Code Patterns

- FastMCP 2.0.0 requires decorators to be called with parentheses:
  `@mcp.tool()`, `@mcp.prompt()`, `@mcp.resource()` instead of `@mcp.tool`,
  `@mcp.prompt`, `@mcp.resource`.
- FastMCP handles event loops internally - use `mcp.run()` directly instead of
  `asyncio.run()` to avoid "Already running asyncio in this thread" errors.
- When debugging dependency issues, check actual error messages rather than
  assuming compatibility problems. The FastMCP error was a bug in the library,
  not a Pydantic version issue.

## Server Implementation

- FastMCP handles the event loop internally, so use `mcp.run()` directly instead
  of `asyncio.run()`. The server runs in stdio mode by default.
- The `/remember` prompt adds new content to AGENTS.md, then cleans up the file
  to remove contradictions and ensure coherence. It does not add timestamps and
  presents the cleaned-up version for user verification before finalizing.

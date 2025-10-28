"""Custom CLI for ericmjl-productivity-mcp.

This is totally optional;
if you want to use it, though,
follow the skeleton to flesh out the CLI to your liking!
Finally, familiarize yourself with Typer,
which is the package that we use to enable this magic.
Typer's docs can be found at:

    https://typer.tiangolo.com
"""

import typer

from .server import run_server

app = typer.Typer()


@app.command()
def hello():
    """Echo the project's name."""
    typer.echo("This project's name is ericmjl-productivity-mcp")


@app.command()
def describe():
    """Describe the project."""
    typer.echo("Personal productivity MCP server.")


@app.command()
def serve(
    transport: str = typer.Option(
        "stdio", "--transport", "-t", help="Transport method (stdio or http)"
    ),
    port: int = typer.Option(
        9247, "--port", "-p", help="Port number for http transport"
    ),
    reload: bool = typer.Option(
        True, "--reload/--no-reload", help="Enable auto-reload for development"
    ),
):
    """Start the MCP server for personal productivity prompts and tools."""
    typer.echo(f"Starting MCP server with {transport} transport...")
    if transport == "http":
        typer.echo(f"Server will be available at http://localhost:{port}")
    typer.echo(f"Auto-reload: {'enabled' if reload else 'disabled'}")

    try:
        run_server(transport=transport, port=port, auto_reload=reload)
    except KeyboardInterrupt:
        typer.echo("\nServer stopped.")


if __name__ == "__main__":
    app()

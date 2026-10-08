from mcp.server.mcpserver import MCPServer

from triage import tools

mcp = MCPServer("oncall-triage")


@mcp.tool()
def get_error_lines(log_path: str) -> list[str]:
    """Return the ERROR lines from a CI build log."""
    return tools.get_error_lines(log_path)


@mcp.tool()
def search_logs(log_path: str, query: str) -> list[str]:
    """Return log lines containing the query text, case-insensitive."""
    return tools.search_logs(log_path, query)


@mcp.tool()
def classify_line(line: str) -> dict:
    """Classify one error line with a Hugging Face zero-shot model."""
    from triage.classify import classify_line as run

    return run(line)


@mcp.tool()
def lookup_runbook(category: str) -> str:
    """Return the runbook step for a failure category."""
    return tools.lookup_runbook(category)


if __name__ == "__main__":
    mcp.run()

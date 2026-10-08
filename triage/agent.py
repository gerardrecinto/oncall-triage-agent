import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parent.parent


def _text(result):
    return result.content[0].text


async def triage(log_path):
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "triage.mcp_server"],
        cwd=str(ROOT),
    )
    findings = []
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            errors = await session.call_tool("get_error_lines", {"log_path": log_path})
            for item in errors.content:
                line = item.text
                cls = await session.call_tool("classify_line", {"line": line})
                label = eval_label(_text(cls))
                book = await session.call_tool("lookup_runbook", {"category": label})
                findings.append({"line": line, "category": label, "runbook": _text(book)})
    return findings


def eval_label(text):
    import json

    return json.loads(text)["label"]


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "data" / "sample_build.log")
    for f in asyncio.run(triage(path)):
        print(f"[{f['category']}] {f['line']}\n   -> {f['runbook']}\n")

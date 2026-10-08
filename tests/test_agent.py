import asyncio
from pathlib import Path

from triage.agent import triage
from triage.classify import DESCRIPTIONS

LOG = str(Path(__file__).resolve().parent.parent / "data" / "sample_build.log")


def test_agent_end_to_end_over_mcp():
    findings = asyncio.run(triage(LOG))
    assert len(findings) == 5
    for f in findings:
        assert f["category"] in DESCRIPTIONS
        assert f["runbook"] != "No runbook for this category."

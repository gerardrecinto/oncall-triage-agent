from pathlib import Path

from triage import tools

LOG = Path(__file__).resolve().parent.parent / "data" / "sample_build.log"


def test_error_lines_only_errors():
    lines = tools.get_error_lines(LOG)
    assert len(lines) == 5
    assert all(" ERROR " in ln for ln in lines)


def test_search_is_case_insensitive():
    assert len(tools.search_logs(LOG, "ARTIFACTORY")) == 1


def test_runbook_known_and_unknown():
    assert "memory" in tools.lookup_runbook("out of memory")
    assert tools.lookup_runbook("nope") == "No runbook for this category."

from pathlib import Path

from triage import tools
from triage.classify import classify_line

LOG = Path(__file__).resolve().parent.parent / "data" / "sample_build.log"
TRUTH = ["out of memory", "network timeout", "authentication failure", "disk full", "test failure"]


def test_zero_shot_accuracy_on_sample_log():
    lines = tools.get_error_lines(LOG)
    hits = sum(classify_line(ln)["label"] == t for ln, t in zip(lines, TRUTH))
    assert hits >= 4

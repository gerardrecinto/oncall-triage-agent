import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def get_error_lines(log_path):
    lines = Path(log_path).read_text().splitlines()
    return [ln for ln in lines if " ERROR " in ln]


def search_logs(log_path, query):
    q = query.lower()
    return [ln for ln in Path(log_path).read_text().splitlines() if q in ln.lower()]


def lookup_runbook(category):
    runbooks = json.loads((DATA / "runbooks.json").read_text())
    return runbooks.get(category, "No runbook for this category.")

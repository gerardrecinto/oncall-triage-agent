# oncall-triage-agent

Small on-call triage tool for CI failures. A Hugging Face zero-shot model (PyTorch) labels error lines from a build log, and an MCP client calls tools on an MCP server to pull errors, classify them, and look up a runbook step.

## What it does

- `triage/mcp_server.py`: MCP server (stdio) exposing four tools: `get_error_lines`, `search_logs`, `classify_line`, `lookup_runbook`.
- `triage/agent.py`: MCP client that starts the server, calls the tools in order for each error line, and prints category plus runbook step.
- `triage/classify.py`: `typeform/distilbert-base-uncased-mnli` through the `transformers` zero-shot pipeline, running on PyTorch.
- `data/sample_build.log`: a synthetic build log written for this repo. It is not a real Apple or Qualcomm log.

## Run

```
python3.12 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m triage.agent
.venv/bin/python -m pytest -q
```

Use an arm64 Python on Apple silicon. An x86_64 Python resolves to an old torch that transformers rejects.

## Results from an actual run

On the 5 error lines in the sample log, the zero-shot model labels 4 correctly. It reads the "container exceeded memory limit, exit code 137" line as an authentication failure. Plain category names scored 3 of 5; descriptive labels plus the template "This CI error means {}." scored 4 of 5. Five lines is too small to say anything about general accuracy.

## Not done

- No LLM API call. The orchestration is a fixed sequence of tool calls, not a model choosing tools. Swapping in Claude tool use against the same MCP server is the next step; it has not been built or run.
- No fine-tuning. The model is used as published.
- Classifier accuracy is only checked on the sample log.

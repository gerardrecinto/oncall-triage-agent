from transformers import pipeline

MODEL = "typeform/distilbert-base-uncased-mnli"
TEMPLATE = "This CI error means {}."
DESCRIPTIONS = {
    "out of memory": "the process was killed for using too much memory",
    "network timeout": "a network connection timed out",
    "authentication failure": "a login or token was rejected as unauthorized",
    "disk full": "the disk has no space left",
    "test failure": "an automated test assertion failed",
}
_BY_DESCRIPTION = {v: k for k, v in DESCRIPTIONS.items()}
_pipe = None


def _get_pipe():
    global _pipe
    if _pipe is None:
        _pipe = pipeline("zero-shot-classification", model=MODEL)
    return _pipe


def classify_line(line):
    msg = line.split(" ERROR ", 1)[-1]
    out = _get_pipe()(
        msg, candidate_labels=list(DESCRIPTIONS.values()), hypothesis_template=TEMPLATE
    )
    return {"label": _BY_DESCRIPTION[out["labels"][0]], "score": round(out["scores"][0], 3)}

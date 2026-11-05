"""Reusable helpers: configuration, Ollama access, formatting and session state."""

import json
import os

import ollama
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

CASES_CSV = os.path.join(DATA_DIR, "sample_cases.csv")
ANALYSIS_FILE = os.path.join(OUTPUT_DIR, "medical_analysis.txt")
STATE_FILE = os.path.join(OUTPUT_DIR, "session_state.json")

OLLAMA_MODEL = "llama3.2:latest"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

LINE = "=" * 64
DASH = "-" * 64

_client = ollama.Client()


class ModelError(Exception):
    """Raised when the local model cannot serve the request."""


def check_model():
    """Verify the Ollama server is reachable and the model is installed."""
    try:
        models = _client.list()
    except Exception:
        raise ModelError("Cannot reach Ollama. Start it with:  ollama serve")
    names = [m.get("model") or m.get("name") for m in models.get("models", [])]
    if OLLAMA_MODEL not in names:
        raise ModelError("Model {} is not installed. Run:  ollama pull {}".format(
            OLLAMA_MODEL, OLLAMA_MODEL.split(":")[0]))
    return names


def ask(system_prompt, user_prompt, temperature=0.3):
    """Send a prompt to the local model served by Ollama."""
    try:
        response = _client.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": user_prompt}],
            options={"temperature": temperature},
        )
    except Exception as exc:
        raise ModelError("Model request failed: {}".format(exc))
    text = response["message"]["content"].strip()
    if not text:
        raise ModelError("The model returned an empty response.")
    return text


def banner(title):
    print(LINE)
    print(title)
    print(LINE)


def wrap(text, width=58):
    """Split a paragraph into lines no longer than the given width."""
    words, line, out = text.split(), "", []
    for word in words:
        if len(line) + len(word) + 1 > width:
            out.append(line)
            line = word
        else:
            line = "{} {}".format(line, word).strip()
    if line:
        out.append(line)
    return out


def preview(text, lines=14, width=62):
    """Print the first few lines of a long block of text."""
    shown = text.split("\n")[:lines]
    for line in shown:
        print(line[:width])
    total = len(text.split("\n"))
    if total > lines:
        print("... ({} more lines)".format(total - lines))


def load_cases():
    """Load the reference symptom cases used for context analysis."""
    if not os.path.exists(CASES_CSV):
        raise ModelError("Dataset not found at {}".format(CASES_CSV))
    return pd.read_csv(CASES_CSV)


# ------------------------------------------------------------- session state
def save_state(state):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE) as f:
        return json.load(f)


def update_state(**kwargs):
    state = load_state()
    state.update(kwargs)
    save_state(state)
    return state


def require(key, message):
    """Return a stored value, or None with a message if it is missing."""
    value = load_state().get(key)
    if not value:
        print(message)
    return value

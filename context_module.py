"""Part C - Context analysis (Q3).

Checks which contextual fields are missing and uses the reference cases to
suggest the details that are usually relevant for similar symptoms.
"""

import pandas as pd

import utils

CONTEXT_FIELDS = [
    ("age", "Age"),
    ("sex", "Sex"),
    ("duration", "Duration of the symptoms"),
    ("severity", "Severity of the symptoms"),
    ("history", "Relevant medical history"),
    ("medication", "Current medications"),
    ("allergies", "Allergies"),
]

EMPTY = ("", "not provided", "na", "n/a", "-")

_model = None


def _embedder():
    """Load the sentence-transformers model once."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(utils.EMBEDDING_MODEL)
    return _model


def missing_fields(state):
    """List the contextual fields the user has not supplied."""
    return [label for key, label in CONTEXT_FIELDS
            if str(state.get(key, "")).strip().lower() in EMPTY]


def similar_cases(symptom_text, top=3):
    """Find the reference cases whose symptoms are closest to the description."""
    from sentence_transformers import util

    frame = utils.load_cases()
    model = _embedder()
    query = model.encode(symptom_text, convert_to_tensor=True)
    corpus = model.encode(frame["symptoms"].tolist(), convert_to_tensor=True)
    scores = util.cos_sim(query, corpus)[0]

    order = scores.argsort(descending=True)[:top]
    rows = []
    for idx in order:
        i = int(idx)
        rows.append({"Case": frame.at[i, "case_id"],
                     "Category": frame.at[i, "category"],
                     "Usual Duration": frame.at[i, "typical_duration"],
                     "Score": round(float(scores[i]), 4)})
    checks = []
    for idx in order:
        for item in str(frame.at[int(idx), "commonly_checked"]).split(","):
            item = item.strip()
            if item and item not in checks:
                checks.append(item)
    return rows, checks


def analyze(verbose=True):
    """Q3 - identify the information that is missing or usually relevant."""
    state = utils.load_state()
    text = state.get("symptom_text", "")
    if not text:
        print("Please enter the symptoms first (option 1).")
        return None

    missing = missing_fields(state)
    rows, checks = similar_cases(text)
    utils.update_state(missing=missing, usually_checked=checks,
                       closest_category=rows[0]["Category"],
                       closest_score=rows[0]["Score"])

    if verbose:
        print("Context Analysis")
        print(utils.DASH)
        print("Reference cases closest to the reported symptoms")
        print(utils.DASH)
        print(pd.DataFrame(rows).to_string(index=False))
        print(utils.DASH)
        print("Contextual fields not provided by the user:")
        if missing:
            for item in missing:
                print("  * {}".format(item))
        else:
            print("  All contextual fields were provided.")
        print(utils.DASH)
        print("Details usually relevant for symptoms of this kind:")
        for item in checks[:8]:
            print("  * {}".format(item))
        print(utils.DASH)
        print("Reference dataset : {} cases".format(len(utils.load_cases())))
        print("Embedding model   : {}".format(utils.EMBEDDING_MODEL))
        print(utils.DASH)
    return missing, checks


if __name__ == "__main__":
    utils.banner("CONTEXT ANALYSIS")
    analyze()

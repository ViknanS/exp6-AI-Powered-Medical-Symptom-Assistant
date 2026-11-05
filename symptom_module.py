"""Part B - Symptom extraction (Q2).

Extracts the individual symptoms from the user's natural-language description.
"""

import re

import utils

SYSTEM = ("You extract symptoms from a patient's own description. "
          "Return ONLY the symptoms, one per line, in plain words, with no numbering, "
          "no bullets, no explanation and no extra text. Use the words the patient used. "
          "Do not add symptoms that are not described.")

NOISE = re.compile(r"^(here|the|these|extracted|symptoms?|based|note|output)\b[: ]", re.I)


def clean_list(text):
    """Turn the model output into a clean list of symptom phrases."""
    items = []
    for line in text.split("\n"):
        line = line.strip(" \t-*0123456789.)•")
        if not line or NOISE.match(line) or len(line) > 60:
            continue
        line = line.rstrip(".").strip()
        if line and line.lower() not in [i.lower() for i in items]:
            items.append(line[0].upper() + line[1:])
    return items


def extract(verbose=True):
    """Q2 - extract the symptoms from the natural-language input."""
    text = utils.require("symptom_text", "Please enter the symptoms first (option 1).")
    if not text:
        return None

    raw = utils.ask(SYSTEM, "Patient description:\n{}\n\nList the symptoms.".format(text),
                    temperature=0.1)
    symptoms = clean_list(raw)
    utils.update_state(symptoms=symptoms, symptom_count=len(symptoms))

    if verbose:
        print("Extracted Symptoms")
        print(utils.DASH)
        print("Patient description:")
        for line in utils.wrap(text, 58):
            print("  {}".format(line))
        print(utils.DASH)
        print("Symptoms identified by the model:")
        for item in symptoms:
            print("  * {}".format(item))
        print(utils.DASH)
        print("Model            : {}".format(utils.OLLAMA_MODEL))
        print("Symptoms found   : {}".format(len(symptoms)))
        print(utils.DASH)
    return symptoms


if __name__ == "__main__":
    utils.banner("SYMPTOM EXTRACTION")
    extract()

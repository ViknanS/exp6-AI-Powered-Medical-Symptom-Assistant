"""Part F - Follow-up questions (Q6)."""

import re

import utils

SYSTEM = ("You write follow-up questions for an informational symptom assistant. "
          "Return ONLY five questions, one per line, numbered 1 to 5. "
          "Each question must be short, factual and answerable by the patient. "
          "Do not give advice, do not suggest a diagnosis and do not add any other text.")

NUMBERED = re.compile(r"^\s*\d+[.)]\s*")


def clean(text):
    """Turn the model output into a clean list of questions."""
    items = []
    for line in text.split("\n"):
        line = NUMBERED.sub("", line.strip()).strip(" -*")
        line = re.sub(r"\*\*", "", line).strip()
        if line.endswith("?") and len(line) < 140:
            items.append(line)
    return items[:5]


def generate(verbose=True):
    """Q6 - generate follow-up questions for the reported symptoms."""
    state = utils.load_state()
    if not state.get("symptom_text"):
        print("Please enter the symptoms first (option 1).")
        return None

    prompt = ("Reported symptoms:\n{}\n\nInformation not provided:\n{}\n\n"
              "Details usually relevant for symptoms of this kind:\n{}\n\n"
              "Write five follow-up questions.").format(
        "\n".join("- {}".format(s) for s in state.get("symptoms", [])) or state["symptom_text"],
        "\n".join("- {}".format(m) for m in state.get("missing", [])) or "- none",
        "\n".join("- {}".format(c) for c in state.get("usually_checked", [])[:6]) or "- none")

    questions = clean(utils.ask(SYSTEM, prompt, temperature=0.3))
    utils.update_state(questions=questions)

    if verbose:
        print("FOLLOW-UP QUESTIONS")
        print(utils.DASH)
        for n, q in enumerate(questions, 1):
            for i, line in enumerate(utils.wrap(q, 56)):
                print("{:>3}. {}".format(n, line) if i == 0 else "     {}".format(line))
        print(utils.DASH)
        print("Questions generated : {}".format(len(questions)))
        print("Model               : {}".format(utils.OLLAMA_MODEL))
        print(utils.DASH)
    return questions


if __name__ == "__main__":
    utils.banner("FOLLOW-UP QUESTIONS")
    generate()

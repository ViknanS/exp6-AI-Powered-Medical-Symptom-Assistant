"""Parts E and H - Symptom analysis and the complete structured response (Q5, Q8)."""

import re

import prompt_module
import safety_module
import utils

HEADINGS = ("Possible Conditions", "Explanation",
            "Additional Information Needed", "Medical Attention")


def split_sections(text):
    """Split the model response into its four requested sections."""
    sections, current = {}, None
    for line in text.split("\n"):
        plain = line.strip().strip("*#").strip().rstrip(":").strip()
        match = next((h for h in HEADINGS if plain.lower() == h.lower()), None)
        if match:
            current = match
            sections[current] = []
        elif current:
            sections[current].append(line.rstrip())
    return {k: "\n".join(v).strip() for k, v in sections.items()}


def bullets(block):
    """Turn a section into a clean list of bullet lines."""
    items = []
    for line in block.split("\n"):
        line = line.strip()
        if line and set(line) <= set("-=_ "):
            continue
        line = line.strip(" \t-*0123456789.)•")
        line = re.sub(r"\*\*", "", line).strip()
        if line:
            items.append(line)
    if len(items) == 1 and len(items[0]) > 160:
        items = [s.strip() for s in re.split(r"(?<=[.])\s+", items[0]) if s.strip()]
    return items


def analyze(verbose=True):
    """Q5 - generate the preliminary symptom analysis with the local model."""
    prompt = utils.load_state().get("prompt") or prompt_module.build_prompt(verbose=False)
    if not prompt:
        return None

    response = utils.ask(prompt_module.SYSTEM, prompt, temperature=0.2)
    sections = split_sections(response)
    utils.update_state(response=response, sections=sections,
                       response_words=len(response.split()))

    if verbose:
        print("Model Response")
        print(utils.DASH)
        print("Model          : {}".format(utils.OLLAMA_MODEL))
        print("Response words : {}".format(len(response.split())))
        print("Sections found : {} of {}".format(len(sections), len(HEADINGS)))
        print(utils.DASH)
        print(response)
        print(utils.DASH)
    return response


def show_conditions(verbose=True):
    """Display the possible conditions the model considered."""
    sections = utils.load_state().get("sections") or {}
    block = sections.get("Possible Conditions", "")
    if not block:
        print("Please analyze the symptoms first (option 3).")
        return None

    items = bullets(block)
    utils.update_state(conditions=items)

    if verbose:
        print("Possible Conditions")
        print(utils.DASH)
        for n, item in enumerate(items, 1):
            for i, line in enumerate(utils.wrap(item, 56)):
                print("{:>3}. {}".format(n, line) if i == 0 else "     {}".format(line))
        print(utils.DASH)
        print("Note:")
        for line in utils.wrap("These symptoms can occur in several conditions. The "
                               "information provided is not sufficient to establish a "
                               "diagnosis.", 58):
            print("  {}".format(line))
        print(utils.DASH)
    return items


def structured(verbose=True):
    """Q8 - present the complete structured response in the required format."""
    state = utils.load_state()
    sections = state.get("sections") or {}
    if not sections:
        print("Please analyze the symptoms first (option 3).")
        return None

    lines = []
    add = lines.append

    add("MEDICAL SYMPTOM ANALYSIS")
    add(utils.DASH)
    add("1. Reported Symptoms:")
    for item in state.get("symptoms", []):
        add("   * {}".format(item))
    add("")
    add("2. Patient Information:")
    for key, label in (("age", "Age"), ("sex", "Sex"), ("duration", "Duration"),
                       ("severity", "Severity"), ("history", "History")):
        add("   {:<10}: {}".format(label, state.get(key, "Not provided")))
    add("")
    add("3. Possible Conditions:")
    for n, item in enumerate(bullets(sections.get("Possible Conditions", "")), 1):
        for i, line in enumerate(utils.wrap(item, 54)):
            add("   {}. {}".format(n, line) if i == 0 else "      {}".format(line))
    add("")
    add("4. Explanation:")
    for item in bullets(sections.get("Explanation", "")):
        for line in utils.wrap(item, 56):
            add("   {}".format(line))
    add("")
    add("5. Missing Information:")
    for item in state.get("missing", []) or ["None"]:
        add("   * {}".format(item))
    add("")
    add("6. Follow-up Questions:")
    for n, q in enumerate(state.get("questions", []) or ["Not generated yet"], 1):
        for i, line in enumerate(utils.wrap(q, 54)):
            add("   {}. {}".format(n, line) if i == 0 else "      {}".format(line))
    add("")
    add("7. Medical Attention Guidance:")
    for line in safety_module.guidance_lines():
        add("   {}".format(line))
    add("")
    add("8. Disclaimer:")
    for line in safety_module.DISCLAIMER:
        add("   {}".format(line))
    add(utils.DASH)

    report = "\n".join(lines)
    utils.update_state(structured=report)

    if verbose:
        print(report)
    return report


if __name__ == "__main__":
    utils.banner("SYMPTOM ANALYSIS")
    if utils.require("symptom_text", "Please enter the symptoms first."):
        analyze()

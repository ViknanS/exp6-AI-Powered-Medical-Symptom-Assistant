"""Part A - User input (Q1).

Collects the patient information and the natural-language symptom description.
"""

import utils

FIELDS = [
    ("age", "Age                     : ", "Not provided"),
    ("sex", "Sex (if relevant)       : ", "Not provided"),
    ("duration", "Duration                : ", "Not provided"),
    ("severity", "Severity (Mild/Moderate/Severe) : ", "Not provided"),
    ("history", "Relevant medical history: ", "Not provided"),
    ("medication", "Current medications     : ", "Not provided"),
    ("allergies", "Allergies               : ", "Not provided"),
    ("additional", "Additional information  : ", "Not provided"),
]


def collect():
    """Q1 - collect the patient information and the symptom description."""
    print("Enter the patient information. Press Enter to skip a field.")
    print(utils.DASH)

    record = {}
    for key, label, default in FIELDS:
        value = input(label).strip()
        record[key] = value or default

    print(utils.DASH)
    print("Describe the symptoms in your own words.")
    record["symptom_text"] = input("Symptoms                : ").strip()

    if not record["symptom_text"]:
        print("A symptom description is required.")
        return None

    utils.update_state(**record)
    return record


def show_symptom_input(verbose=True):
    """Display the natural-language symptom description that was entered."""
    state = utils.load_state()
    text = state.get("symptom_text", "")
    if not text:
        print("No symptom description found. Use option 2 first.")
        return None

    if verbose:
        print("Symptom Input")
        print(utils.DASH)
        print("Entered in natural language by the user:")
        print()
        for line in utils.wrap(text, 58):
            print("  {}".format(line))
        print()
        print("Characters : {}".format(len(text)))
        print("Words      : {}".format(len(text.split())))
        print(utils.DASH)
    return text


if __name__ == "__main__":
    utils.banner("USER INPUT")
    if collect():
        print()
        show_symptom_input()

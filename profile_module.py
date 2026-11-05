"""Part A - Patient profile (Q1).

Validates the collected information and displays it as a patient profile.
"""

import utils

LABELS = [
    ("age", "Age"),
    ("sex", "Sex"),
    ("duration", "Duration"),
    ("severity", "Severity"),
    ("history", "Medical History"),
    ("medication", "Current Medication"),
    ("allergies", "Allergies"),
    ("additional", "Additional Information"),
]

SEVERITIES = ("mild", "moderate", "severe")


def build_profile():
    """Normalise the collected fields into a patient profile."""
    state = utils.load_state()
    profile = {key: str(state.get(key, "Not provided")).strip() or "Not provided"
               for key, _ in LABELS}

    age = profile["age"]
    profile["age_valid"] = age.isdigit() and 0 < int(age) < 120
    profile["severity_valid"] = profile["severity"].lower() in SEVERITIES
    utils.update_state(profile=profile)
    return profile


def show_profile(verbose=True):
    """Display the patient profile neatly."""
    if not utils.require("symptom_text", "Please enter the patient details first (option 1)."):
        return None
    profile = build_profile()

    if verbose:
        print("Patient Information")
        print(utils.DASH)
        for key, label in LABELS:
            print("{:<24}: {}".format(label, profile[key]))
        print(utils.DASH)
        print("Age field valid      : {}".format("yes" if profile["age_valid"] else "not numeric"))
        print("Severity recognised  : {}".format(
            "yes" if profile["severity_valid"] else "not one of Mild/Moderate/Severe"))
        print("Fields provided      : {} of {}".format(
            sum(1 for k, _ in LABELS if profile[k] != "Not provided"), len(LABELS)))
        print(utils.DASH)
    return profile


if __name__ == "__main__":
    utils.banner("PATIENT PROFILE")
    show_profile()

"""Parts G and I - Medical attention guidance and disclaimer (Q7, Q9)."""

import utils

URGENT_WORDS = (
    "chest pain", "difficulty breathing", "breathless", "shortness of breath",
    "unconscious", "fainting", "slurred speech", "weakness on one side",
    "severe bleeding", "seizure", "blue lips", "confusion",
)

GENERAL = ("If symptoms are severe, rapidly worsening, or concerning, seek "
           "appropriate professional medical care.")

ESCALATION = ("The description mentions symptoms that are generally treated as "
              "urgent. Please contact emergency medical services or attend an "
              "emergency department without waiting for this analysis.")

DISCLAIMER = [
    "This AI-generated response is intended for",
    "educational and informational purposes only.",
    "It is not a medical diagnosis and does not",
    "replace advice from a qualified healthcare",
    "professional.",
    "For serious, worsening or urgent symptoms,",
    "seek appropriate medical care.",
]


def flagged_terms():
    """Terms in the user's description that are generally treated as urgent."""
    text = utils.load_state().get("symptom_text", "").lower()
    return [word for word in URGENT_WORDS if word in text]


def guidance_lines():
    """The medical-attention wording for the current case."""
    lines = utils.wrap(GENERAL, 56)
    if flagged_terms():
        lines += [""] + utils.wrap(ESCALATION, 56)
    state = utils.load_state()
    severity = str(state.get("severity", "Not provided"))
    lines += ["",
              "Severity reported by the user : {}".format(severity),
              "This system does not make a clinical triage decision."]
    return lines


def guidance(verbose=True):
    """Q7 - display the medical attention guidance."""
    if not utils.require("symptom_text", "Please enter the symptoms first (option 1)."):
        return None
    lines = guidance_lines()
    utils.update_state(guidance=lines, urgent_terms=flagged_terms())

    if verbose:
        print("MEDICAL ATTENTION")
        print(utils.DASH)
        for line in lines:
            print(line)
        print(utils.DASH)
        terms = flagged_terms()
        print("Urgent terms detected in the description : {}".format(
            ", ".join(terms) if terms else "none"))
        print(utils.DASH)
    return lines


def disclaimer(verbose=True):
    """Q9 - display the required disclaimer."""
    if verbose:
        print("DISCLAIMER")
        print(utils.DASH)
        for line in DISCLAIMER:
            print(line)
        print(utils.DASH)
    return DISCLAIMER


if __name__ == "__main__":
    utils.banner("SAFETY AND DISCLAIMER")
    guidance()
    print()
    disclaimer()

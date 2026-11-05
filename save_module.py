"""Part J - Save the analysis (Q10)."""

import datetime
import os

import analysis_module
import utils


def save(verbose=True):
    """Q10 - save the generated analysis to outputs/medical_analysis.txt."""
    state = utils.load_state()
    if not state.get("sections"):
        print("Please analyze the symptoms first (option 3).")
        return None

    report = state.get("structured") or analysis_module.structured(verbose=False)

    lines = [
        "AI-POWERED MEDICAL SYMPTOM ASSISTANT - ANALYSIS REPORT",
        "=" * 55,
        "Date  : {}".format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M")),
        "Model : {}".format(utils.OLLAMA_MODEL),
        "=" * 55,
        "",
        report,
        "",
        "RAW MODEL RESPONSE",
        "-" * 55,
        state.get("response", ""),
        "",
    ]

    try:
        os.makedirs(utils.OUTPUT_DIR, exist_ok=True)
        with open(utils.ANALYSIS_FILE, "w") as f:
            f.write("\n".join(lines))
    except OSError as exc:
        raise utils.ModelError("Could not save the analysis: {}".format(exc))

    if verbose:
        print("Analysis report saved successfully.")
        print(utils.DASH)
        print("File        : {}".format(utils.ANALYSIS_FILE))
        print("Lines       : {}".format(len(lines)))
        print("Characters  : {}".format(len("\n".join(lines))))
        print("Symptoms    : {}".format(len(state.get("symptoms", []))))
        print("Conditions  : {}".format(len(state.get("conditions", []))))
        print("Questions   : {}".format(len(state.get("questions", []))))
        print(utils.DASH)
    return utils.ANALYSIS_FILE


if __name__ == "__main__":
    utils.banner("SAVE ANALYSIS REPORT")
    save()

"""Part D - Prompt generation (Q4)."""

import utils

SYSTEM = ("You are an informational medical symptom assistant for a student laboratory "
          "exercise. You never give a diagnosis and you never tell the user that a "
          "condition is confirmed. You describe possibilities in cautious language, you "
          "say plainly when the information is not sufficient, and you always encourage "
          "the user to consult a qualified healthcare professional. You use only the "
          "information the user has provided and you do not invent details.")

TEMPLATE = """Analyse the reported symptoms below.

Patient information
-------------------
Age        : {age}
Sex        : {sex}
Duration   : {duration}
Severity   : {severity}
History    : {history}
Medication : {medication}
Allergies  : {allergies}
Additional : {additional}

Symptoms described by the patient
---------------------------------
{symptom_text}

Symptoms extracted from that description
----------------------------------------
{symptoms}

Information that was not provided
---------------------------------
{missing}

Produce the analysis using exactly these headings, in this order:
Possible Conditions
Explanation
Additional Information Needed
Medical Attention

Rules you must follow:
1. Do not give a diagnosis and do not present any condition as confirmed.
2. Describe possible conditions as possibilities only, and say that the information
   provided is not sufficient to establish a diagnosis.
3. Explain the reasoning at a general level only.
4. Use only the information given above. Do not invent symptoms, test results or history.
5. Under Medical Attention, use cautious wording and advise professional medical care for
   severe, worsening or concerning symptoms.
6. Keep the whole response under 300 words. Do not add any heading other than the four
   listed above.
"""


def build_prompt(verbose=True):
    """Q4 - construct the analysis prompt for the model."""
    state = utils.load_state()
    if not state.get("symptom_text"):
        print("Please enter the symptoms first (option 1).")
        return None

    prompt = TEMPLATE.format(
        age=state.get("age", "Not provided"),
        sex=state.get("sex", "Not provided"),
        duration=state.get("duration", "Not provided"),
        severity=state.get("severity", "Not provided"),
        history=state.get("history", "None reported"),
        medication=state.get("medication", "None reported"),
        allergies=state.get("allergies", "None reported"),
        additional=state.get("additional", "None reported"),
        symptom_text=state.get("symptom_text", ""),
        symptoms="\n".join("- {}".format(s) for s in state.get("symptoms", [])) or "- not extracted",
        missing="\n".join("- {}".format(m) for m in state.get("missing", [])) or "- none",
    )

    utils.update_state(prompt=prompt, prompt_chars=len(prompt))

    if verbose:
        print("Prompt Generation")
        print(utils.DASH)
        print("System role    : informational medical symptom assistant")
        print("Headings asked : Possible Conditions, Explanation,")
        print("                 Additional Information Needed, Medical Attention")
        print("Safety rules   : 6 (no diagnosis, no invented information)")
        print("Prompt chars   : {}".format(len(prompt)))
        print("Prompt words   : {}".format(len(prompt.split())))
        print(utils.DASH)
        print("Generated prompt (first lines)")
        print(utils.DASH)
        utils.preview(prompt, lines=22)
        print(utils.DASH)
    return prompt


if __name__ == "__main__":
    utils.banner("PROMPT GENERATION")
    build_prompt()

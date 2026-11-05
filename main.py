"""Part K - Complete AI-Powered Medical Symptom Assistant (Q11).

Menu driven application that keeps running until the user exits.
"""

import analysis_module
import context_module
import input_module
import profile_module
import prompt_module
import question_module
import safety_module
import save_module
import symptom_module
import utils

MENU = """  1. Enter Patient Information
  2. Enter Symptoms
  3. Analyze Symptoms
  4. Generate Follow-up Questions
  5. Display Possible Conditions
  6. Display Medical Attention Guidance
  7. Display Disclaimer
  8. Save Report
  9. Exit"""


def home_screen():
    print(utils.LINE)
    print("      AI-POWERED MEDICAL SYMPTOM ASSISTANT")
    print("      Powered by {} running locally on Ollama".format(utils.OLLAMA_MODEL))
    print(utils.LINE)
    print("  Informational only - this is not a medical diagnosis.")
    print(utils.LINE)
    print(MENU)
    print(utils.LINE)


def handle(choice):
    if choice == "1":
        if input_module.collect():
            print()
            profile_module.show_profile()

    elif choice == "2":
        input_module.show_symptom_input()

    elif choice == "3":
        if not utils.require("symptom_text", "Please enter the patient details first (option 1)."):
            return
        symptom_module.extract()
        print()
        context_module.analyze()
        print()
        prompt_module.build_prompt()
        print()
        analysis_module.analyze()

    elif choice == "4":
        if utils.require("response", "Please analyze the symptoms first (option 3)."):
            question_module.generate()

    elif choice == "5":
        analysis_module.show_conditions()

    elif choice == "6":
        safety_module.guidance()

    elif choice == "7":
        safety_module.disclaimer()

    elif choice == "8":
        save_module.save()

    else:
        print("Invalid choice. Please enter a number between 1 and 9.")


def main():
    try:
        utils.check_model()
    except utils.ModelError as exc:
        print(utils.LINE)
        print("  AI-POWERED MEDICAL SYMPTOM ASSISTANT")
        print(utils.LINE)
        print(exc)
        return

    home_screen()

    while True:
        try:
            choice = input("Enter your choice : ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not choice:
            continue
        if choice == "9" or choice.lower() == "exit":
            print("\nThank you for using the Medical Symptom Assistant. Goodbye!")
            break

        print()
        try:
            handle(choice)
        except utils.ModelError as exc:
            print("Error: {}".format(exc))
        print(utils.LINE)


if __name__ == "__main__":
    main()

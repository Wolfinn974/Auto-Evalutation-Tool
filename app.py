import sys
from eval_core.engine import EvaluationEngine
from eval_core.utils import safe_print, log
from eval_core.admin import AdminMenu  # You’ll implement admin next

#redacted in french for my students (in english for my part) please modify it in your prefered langage.

def main():
    safe_print("===========================================")
    safe_print("      🔵 Python Auto-Evaluator (v1)        ")
    safe_print("===========================================")
    safe_print("\nBienvenue ! Ceci est un logiciel qui fera votre évaluation.")
    safe_print("Veuillez entrez votre nom ci dessous.\n")

    # -----------------------------------------
    # GET STUDENT / USER NAME
    # -----------------------------------------
    student_name = input("Entrez votre nom: ").strip()

    if not student_name:
        safe_print("❌ Le nom ne peut pas être vide.")
        sys.exit(1)

    log(f"Application launched by: {student_name}")

    # -----------------------------------------
    # TEACHER MODE
    # -----------------------------------------
    if student_name.lower() in ["teacher", "admin", "prof"]:
        safe_print("\n🔐 Entering ADMIN MODE...\n")
        admin = AdminMenu()
        admin.start()
        return

    # -----------------------------------------
    # STUDENT MODE
    # -----------------------------------------
    safe_print(f"\n👋 Hello {student_name}!")
    safe_print("Ton evaluation commence maintenant.")
    safe_print("Suis les instructions.\n")

    try:
        engine = EvaluationEngine(student_name)
        engine.run()

        safe_print("\n===========================================")
        safe_print("           ✅ Evaluation finished!          ")
        safe_print("===========================================\n")

    except KeyboardInterrupt:
        safe_print("\n⚠️ Evaluation aborted by user.")
        log(f"Evaluation interrupted by {student_name}")

    except Exception as e:
        safe_print("\n❌ Une erreur est apparue. Veuillez appelez votre professeur.")
        log(f"[CRITICAL ERROR] {e}")

if __name__ == "__main__":
    main()
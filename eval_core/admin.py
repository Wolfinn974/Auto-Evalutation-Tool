import os
import json
from eval_core.utils import safe_print, log

RESULTS_DIR = "results"
LOG_FILE = "logs/system.log"

class AdminMenu:

    def __init__(self):
        # Make sure results folder exists
        if not os.path.isdir(RESULTS_DIR):
            os.mkdir(RESULTS_DIR)

    # -----------------------------------------------------
    # Main loop
    # -----------------------------------------------------

    def start(self):
        safe_print("===========================================")
        safe_print("              🔐 ADMIN MODE                ")
        safe_print("===========================================\n")

        while True:
            self.display_menu()
            choice = input("> ").strip()

            if choice == "1":
                self.list_students()

            elif choice == "2":
                self.show_student_results()

            elif choice == "3":
                self.show_system_logs()

            elif choice == "4":
                safe_print("\n🔙 Leaving admin mode...")
                break

            else:
                safe_print("❌ Invalid choice. Try again.\n")

    # -----------------------------------------------------
    # Menu options display
    # -----------------------------------------------------

    def display_menu(self):
        safe_print("\nChoose an option:")
        safe_print("1️⃣  List all students evaluated")
        safe_print("2️⃣  View results of a specific student")
        safe_print("3️⃣  View system logs")
        safe_print("4️⃣  Exit admin mode\n")

    # -----------------------------------------------------
    # Option 1 — List students
    # -----------------------------------------------------

    def list_students(self):
        safe_print("\n📁 Students evaluated:")

        dirs = [d for d in os.listdir(RESULTS_DIR)
                if os.path.isdir(os.path.join(RESULTS_DIR, d))]

        if not dirs:
            safe_print("⚠️ No student results found yet.\n")
            return

        for d in dirs:
            safe_print(f" - {d}")

        safe_print("")

    # -----------------------------------------------------
    # Option 2 — Show a student's results.json
    # -----------------------------------------------------

    def show_student_results(self):
        student = input("\nEnter student name: ").strip()

        path = os.path.join(RESULTS_DIR, student, "results.json")

        if not os.path.exists(path):
            safe_print(f"❌ No results found for '{student}'.")
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            safe_print("\n===========================================")
            safe_print(f"📊 Results for: {student}")
            safe_print("===========================================\n")

            safe_print(f"QCM Score : {data['qcm_score']}")
            safe_print(f"Total Score : {data['total_score']}")
            safe_print(f"Passed : {'✅ YES' if data['passed'] else '❌ NO'}\n")

            safe_print("🧪 Exercises results:")
            for exo in data["exercises"]:
                status = "✅ OK" if exo["success"] else "❌ KO"
                safe_print(f" - {exo['exercise']:25} {status} ({exo['points']} pts)")

            safe_print("\n===========================================\n")

        except Exception as e:
            safe_print("❌ Error reading results file.")
            log(f"[ADMIN ERROR] Failed to load results for {student}: {e}")

    # -----------------------------------------------------
    # Option 3 — Show system logs
    # -----------------------------------------------------

    def show_system_logs(self):
        if not os.path.exists(LOG_FILE):
            safe_print("⚠️ No system logs found.")
            return

        safe_print("\n======= 📝 SYSTEM LOGS =======\n")

        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                for line in f.readlines()[-50:]:  # show last 50 lines
                    safe_print(line.rstrip())

            safe_print("\n==============================\n")

        except Exception as e:
            safe_print("❌ Error opening system logs.")
            log(f"[ADMIN ERROR] Failed to open system.log: {e}")
import os
import json
from eval_core.utils import safe_print, log
from eval_core.file_loader import StudentFileManager
from eval_core.sandbox_runner import SandboxRunner
from eval_core.scoring import ScoringSystem
from eval_core.comparator import Comparator
from eval_core.cooldown import CooldownManager
from eval_core.git_manager import GitManager


class EvaluationEngine:

    def __init__(self, student_name):
        self.student = student_name

        # Load config files
        self.config = self._load_json("config/eval_config.json")
        self.qcm_data = self._load_json("config/qcm.json")
        self.roasts = self._load_json("config/roasts.json")
        self.exercises_data = self._load_json("config/exercises.json")

        # Core systems
        self.file_manager = StudentFileManager(self.student)
        self.sandbox = SandboxRunner()
        self.scoring = ScoringSystem(self.config)
        self.comparator = Comparator()
        self.cooldown = CooldownManager(self.config)

        # Git sync
        self.git = GitManager(self.config["git_repo"])
        self.git.clone_if_needed()

        # Result structure
        self.results = {
            "student": self.student,
            "qcm_score": 0,
            "exercises": [],
            "total_score": 0,
            "passed": False
        }

        log(f"Starting evaluation session for {self.student}")


    # ---------------------------------------------------------
    # Load JSON helper
    # ---------------------------------------------------------
    def _load_json(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing config file: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ---------------------------------------------------------
    # Load test.json for an exercise
    # ---------------------------------------------------------
    def _load_tests(self, exo_name):
        path = os.path.join("exercises", exo_name, "test.json")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing test.json for {exo_name}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)["tests"]

    # ---------------------------------------------------------
    # RUN FULL EVALUATION
    # ---------------------------------------------------------
    def run(self):
        self.prepare_session()
        self.run_qcm()
        self.run_exercises()
        self.finalize()


    # ---------------------------------------------------------
    # PREPARE FOLDERS
    # ---------------------------------------------------------
    def prepare_session(self):
        self.file_manager.prepare_student_directory()


    # ---------------------------------------------------------
    # QCM SECTION
    # ---------------------------------------------------------
    def run_qcm(self):
        safe_print("\n===== QCM =====")

        questions = self.qcm_data["questions"][: self.config["qcm_count"]]
        total_qcm_points = 0

        for q in questions:
            safe_print(f"\n{q['question']}")
            for choice in q["choices"]:
                safe_print("  " + choice)

            ans = input("\nYour answer: ").strip().upper()

            if ans == q["answer"]:
                total_qcm_points += q["points"]
            else:
                roast = self.cooldown.roast("qcm_wrong", self.roasts)
                safe_print(roast)

        self.results["qcm_score"] = total_qcm_points
        self.scoring.set_qcm_points(total_qcm_points)
        log(f"QCM scored {total_qcm_points} pts")


    # ---------------------------------------------------------
    # EXERCISES SECTION
    # ---------------------------------------------------------
    def run_exercises(self):
        safe_print("\n===== EXERCISES =====")

        selected_exos = self.exercises_data["exercises"][: self.config["exercise_count"]]

        for exo in selected_exos:
            exo_name = exo["name"]
            language = exo["language"]
            points = exo["points"]

            safe_print(f"\n--- Exercise: {exo_name} ---")

            # Show description
            desc_path = os.path.join("exercises", exo_name, "description.md")
            if os.path.exists(desc_path):
                with open(desc_path, "r", encoding="utf-8") as f:
                    safe_print(f.read())

            attempt = 1

            while True:
                # WAIT FOR FILE
                file_path = self.file_manager.wait_for_submission(exo_name)

                if file_path is None:
                    safe_print(self.cooldown.roast("wrong_filename", self.roasts, exo_name))
                    self.cooldown.apply_penalty(attempt)
                    attempt += 1
                    continue

                # LOAD TESTS
                tests = self._load_tests(exo_name)

                all_passed = True

                for test in tests:
                    input_data = test.get("input", "")
                    expected = test["output"]

                    result = self.sandbox.run(
                        file_path=file_path,
                        language=language,
                        input_data=input_data
                    )

                    # Runtime fail?
                    if result.exit_code != 0 or result.stderr.strip() != "":
                        log(f"Runtime error: {result.stderr}")
                        safe_print(self.cooldown.roast("runtime", self.roasts, exo_name))
                        self.cooldown.apply_penalty(attempt)
                        attempt += 1
                        all_passed = False
                        break

                    # Output comparison
                    if not self.comparator.compare(result.stdout, expected):
                        log("Wrong output.")
                        safe_print(self.cooldown.roast("wrong_output", self.roasts, exo_name))
                        self.cooldown.apply_penalty(attempt)
                        attempt += 1
                        all_passed = False
                        break

                # SUCCESS !!
                if all_passed:
                    safe_print(f"✔️ Correct ! +{points} pts")
                    self.results["exercises"].append({
                        "exercise": exo_name,
                        "success": True,
                        "points": points
                    })
                    self.scoring.add_points(points)
                    break


    # ---------------------------------------------------------
    # FINALIZATION
    # ---------------------------------------------------------
    def finalize(self):
        total = self.scoring.total_points()
        self.results["total_score"] = total
        self.results["passed"] = (total >= self.config["passing_score"])

        self.file_manager.save_results(self.results)
        self.git.push_results(self.student)

        safe_print("\n===== END OF EVALUATION =====")
        safe_print(f"Total score: {total}")
        safe_print("PASSED!" if self.results["passed"] else "FAILED...")
import time
import json
import random
import os
from datetime import datetime, timedelta

from eval_core.qcm import QCMEngine
from eval_core.file_loader import StudentFileManager
from eval_core.sandbox_runner import SandboxRunner
from eval_core.comparator import Comparator
from eval_core.cooldown import CooldownManager
from eval_core.scoring import ScoringSystem
from eval_core.utils import log

class EvaluationEngine:

    def __init__(self, student_name):
        self.student = student_name
        self.start_time = None
        self.end_time = None

        # Load configs
        self.config = self._load_json("config/eval_config.json")
        self.exo_bank = self._load_json("config/exercises.json")["exercises"]
        self.qcm_bank = self._load_json("config/qcm.json")
        self.roasts = self._load_json("config/roasts.json")#TODO

        # Points
        self.scoring = ScoringSystem(self.config)#TODO

        # Components
        self.qcm_engine = QCMEngine(self.qcm_bank, self.config)#done
        self.file_manager = StudentFileManager(self.student)#TODO
        self.runner = SandboxRunner()#TODO
        self.cooldown = CooldownManager(self.config)#TODO

        # Prepare output
        self.selected_exercises = []
        self.results = {
            "student": self.student,
            "qcm_score": 0,
            "exercises": [],
            "total_score": 0,
            "passed": False
        }

    # -----------------------------
    # INITIAL SETUP
    # -----------------------------

    def _load_json(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def prepare_session(self):
        log(f"Starting evaluation session for {self.student}")
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(minutes=self.config["duration_minutes"])

        # Ensure student folder exists
        self.file_manager.prepare_student_directory()#mkdir

        # Select QCM
        self.qcm_engine.pick_questions()

        # Select exercises
        self.selected_exercises = self.pick_exercises()

    # -----------------------------
    # SELECT EXERCISES
    # -----------------------------

    def pick_exercises(self):
        count = self.config["exercise_count"]
        # Weighted random pick
        population = self.exo_bank
        weights = [exo["points"] for exo in population]
        chosen = random.choices(population, weights=weights, k=count)

        log(f"Selected exercises: {', '.join([c['name'] for c in chosen])}")
        return chosen

    # -----------------------------
    # RUN QCM
    # -----------------------------

    def run_qcm(self):
        log("Running QCM...")
        qcm_score = self.qcm_engine.run()

        self.results["qcm_score"] = qcm_score
        log(f"QCM complete: {qcm_score} points")

    # -----------------------------
    # RUN EXERCISES
    # -----------------------------

    def run_exercises(self):
        comparator = Comparator()

        for exo in self.selected_exercises:

            exo_name = exo["name"]
            log(f"Evaluating exercise: {exo_name}")

            success = False
            attempt = 1

            while datetime.now() < self.end_time:

                # Load student file or wait for submission
                file_path = self.file_manager.wait_for_submission(exo_name)

                # Check filename validity
                if not self.file_manager.check_expected_filename(exo_name, file_path):#security
                    roast = self.cooldown.roast("wrong_filename", self.roasts)
                    log(f"Wrong filename for {exo_name}. Roast: {roast}")
                    self.cooldown.apply_penalty(attempt)
                    attempt += 1
                    continue

                # Execute file
                output = self.runner.run(file_path, exo["language"])

                # Runtime error
                if output["error"]:
                    roast = self.cooldown.roast("runtime_error", self.roasts, exo_name)
                    log(f"Runtime error: {roast}")
                    self.cooldown.apply_penalty(attempt)
                    attempt += 1
                    continue

                # Compare with expected
                if comparator.compare(exo_name, output["stdout"]):
                    # Success!
                    points = exo["points"]
                    self.results["exercises"].append({
                        "exercise": exo_name,
                        "success": True,
                        "points": points
                    })
                    self.scoring.add_points(points)
                    log(f"{exo_name} success ! Earned {points} points.")
                    success = True
                    break
                else:#failed oh man ! :(
                    roast = self.cooldown.roast("wrong_output", self.roasts, exo_name)
                    log(f"{exo_name} KO: {roast}")
                    self.cooldown.apply_penalty(attempt)
                    attempt += 1

            # If time ran out or never succeeded
            if not success:
                self.results["exercises"].append({
                    "exercise": exo_name,
                    "success": False,
                    "points": 0
                })
                log(f"{exo_name} FAILED (time or errors)")

    # -----------------------------
    # FINAL SCORING & EXPORT
    # -----------------------------

    def finalize(self):
        total = self.scoring.total_points()
        self.results["total_score"] = total
        self.results["passed"] = total >= self.config["passing_score"]

        log(f"Final score: {total} — Passed: {self.results['passed']}")

        # Export results
        self.file_manager.save_results(self.results)

    # -----------------------------
    # MAIN PIPELINE
    # -----------------------------

    def run(self):
        self.prepare_session()
        self.run_qcm()
        self.run_exercises()
        self.finalize()
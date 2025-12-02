import os
import time
import json
from datetime import datetime
from eval_core.utils import log

class StudentFileManager:
    #TODO: strict regex
    SAFE_NAME_REGEX = r"^[a-zA-Z0-9_\-\.]+$"

    def __init__(self, student_name):
        self.student = student_name
        self.base_dir = os.path.abspath("results")
        self.student_dir = os.path.join(self.base_dir, self.student)

    # ------------------------------------------------
    # PREPARE FOLDER
    # ------------------------------------------------

    def prepare_student_directory(self):
        """
        Create results/<student>/ if missing.
        """
        if not os.path.isdir(self.base_dir):
            os.mkdir(self.base_dir)#cmd to make dir

        if not os.path.isdir(self.student_dir):
            os.mkdir(self.student_dir)#cmd to make dir

        log(f"Created/checked student directory: {self.student_dir}")

    # ------------------------------------------------
    # EXPECTED FILENAME FOR EXERCISE
    # ------------------------------------------------

    def _load_expected_filenames(self, exo_name):
        path = os.path.join("exercises", exo_name, "expected_files.json")
        #Security if no path
        if not os.path.exists(path):
            raise FileNotFoundError(f"[SECURITY] Missing expected_files.json for {exo_name}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data["filenames"]

    # ------------------------------------------------
    # VERIFY FILENAME
    # ------------------------------------------------

    def check_expected_filename(self, exo_name, file_path):
        expected = self._load_expected_filenames(exo_name)
        #TODO: ADD SECURITY
        filename = os.path.basename(file_path)

        # Must match EXACT expected filename
        if filename not in expected:
            log(f"Filename '{filename}' does not match expected {expected}")
            return False

        return True

    # ------------------------------------------------
    # WAIT FOR SUBMISSION
    # ------------------------------------------------

    def wait_for_submission(self, exo_name):
        """
        Waits for the student to type 'submit'.
        Then checks once if a valid file exists.
        If not found → return None so the engine can restart the prompt.
        """

        print("\n► When your file is ready, type: submit")
        print("► Your file must be placed in:", self.student_dir)

        # Wait for command
        while True:
            cmd = input("> ").strip().lower()
            if cmd == "submit":
                break
            print("Type 'submit' when your solution file is ready.")

        # After submit → check once
        expected_files = self._load_expected_filenames(exo_name)

        for fname in os.listdir(self.student_dir):
            if fname in expected_files:
                path = os.path.join(self.student_dir, fname)
                if os.path.isfile(path):
                    log(f"Found submitted file: {path}")
                    return path

        # If no file found → return None instead of looping forever
        print("\n⚠️ File not found. Make sure you placed:", expected_files)
        return None

    # ------------------------------------------------
    # SAVE RESULTS JSON
    # ------------------------------------------------

    def save_results(self, results_dict):
        """
        Save result.json inside student's folder.
        """
        path = os.path.join(self.student_dir, "results.json")

        with open(path, "w", encoding="utf-8") as f:
            json.dump(results_dict, f, indent=4)

        log(f"Saved results for {self.student} at {path}")
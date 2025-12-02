import json
import os
import re
from eval_core.utils import log

class Comparator:

    SAFE_NAME_REGEX = r"^[a-zA-Z0-9_\-]+$"

    def __init__(self, tests_path="exercises"):
        """
        tests_path : root folder of all exercises.
        """
        self.tests_root = tests_path
        # Safety: ensure directory exists
        if not os.path.isdir(self.tests_root):
            raise FileNotFoundError(
                f"[SECURITY] Tests root directory not found: {self.tests_root}"
            )

    # -----------------------------------------
    # LOAD TESTS
    # -----------------------------------------

    def load_tests(self, exercise_name):
        """
        Loads test.json for the given exercise.
        """
        # SECURITY CHECK 1 — validate name
        if not re.match(self.SAFE_NAME_REGEX, exercise_name):
            raise ValueError(
                f"[SECURITY] Invalid exercise name '{exercise_name}' (potential path traversal)"
            )

        # SECURITY CHECK 2 — build safe path
        exo_dir = os.path.join(self.tests_root, exercise_name)
        exo_dir = os.path.abspath(exo_dir)

        # SECURITY CHECK 3 — ensure path is INSIDE tests_root
        if not exo_dir.startswith(self.tests_root):
            raise PermissionError("[SECURITY] Attempt to access outside tests directory")

        # SECURITY CHECK 4 — ensure directory exists
        if not os.path.isdir(exo_dir):
            raise FileNotFoundError(
                f"[SECURITY] Exercise directory missing: {exo_dir}"
            )

        # SECURITY CHECK 5 — ensure test.json exists
        path = os.path.join(exo_dir, "test.json")

        if not os.path.exists(path):
            raise FileNotFoundError(
                f"[SECURITY] test.json not found for exercise '{exercise_name}'"
            )

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data["tests"]

    # -----------------------------------------
    # NORMALIZE OUTPUT
    # -----------------------------------------

    def _normalize(self, s):
        """
        Clean & normalize output to avoid false negatives.
        """
        if s is None:
            return ""

        # Remove trailing spaces
        s = s.rstrip()

        # Ensure final newline consistency
        if not s.endswith("\n"):
            s += "\n"

        return s

    # -----------------------------------------
    # COMPARE STUDENT OUTPUT TO EXPECTED
    # -----------------------------------------

    def compare(self, got, expected):
        got_norm = self._normalize(got)
        exp_norm = self._normalize(expected)
        return got_norm == exp_norm
    #TODO:    add strict mode

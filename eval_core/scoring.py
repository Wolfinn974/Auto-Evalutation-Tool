from eval_core.utils import log

class ScoringSystem:

    def __init__(self, config):
        self.config = config
        self.points_qcm = 0
        self.points_exercises = 0

    # ---------------------------------------------------------
    # QCM POINTS
    # ---------------------------------------------------------

    def set_qcm_points(self, pts):
        """
        Set the score obtained from the QCM engine.
        """
        self.points_qcm = pts
        log(f"Scoring: QCM points set to {pts}")

    # ---------------------------------------------------------
    # EXERCISE POINTS
    # ---------------------------------------------------------

    def add_points(self, pts):
        """
        Add points for a successfully validated exercise.
        """
        if not isinstance(pts, (int, float)):
            log(f"[WARNING] Invalid points type: {pts} — forcing 0")
            pts = 0

        self.points_exercises += pts
        log(f"Scoring: +{pts} points (Exercises total = {self.points_exercises})")

    # ---------------------------------------------------------
    # TOTAL POINTS
    # ---------------------------------------------------------

    def total_points(self):
        total = self.points_qcm + self.points_exercises
        log(f"Scoring: Total = {total} (QCM={self.points_qcm}, EXO={self.points_exercises})")
        return total

    # ---------------------------------------------------------
    # PASS / FAIL
    # ---------------------------------------------------------

    def passed(self):
        total = self.total_points()
        required = self.config["passing_score"]
        return total >= required

#TODO: add coeff for level of exercises,
# add malus and bonus
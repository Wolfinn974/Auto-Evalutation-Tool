import subprocess
import os
from eval_core.utils import log

class GitManager:

    def __init__(self, repo_url, repo_dir="submissions"):
        self.repo_url = repo_url
        self.repo_dir = repo_dir
        self.repo_path = os.path.abspath(repo_dir)

    # ---------------------------------------------------------
    # Run git command safely (no shell injection)
    # ---------------------------------------------------------

    def _git(self, args):
        """
        Run a git command using subprocess safely.
        """
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.repo_path if os.path.isdir(self.repo_path) else None,
                capture_output=True,
                text=True,
                shell=False
            )

            if result.returncode != 0:
                log(f"[GIT ERROR] {' '.join(args)} -> {result.stderr}")
            else:
                log(f"[GIT] {' '.join(args)}")

        except Exception as e:
            log(f"[GIT EXCEPTION] {e}")

    # ---------------------------------------------------------
    # Clone repo if missing
    # ---------------------------------------------------------

    def clone_if_needed(self):
        if os.path.isdir(self.repo_path):
            log("Repo already exists, pulling latest changes.")
            #self._git(["pull"])
            return

        log(f"Cloning repository from {self.repo_url}...")
        subprocess.run(
            ["git", "clone", self.repo_url, self.repo_dir],
            capture_output=True,
            text=True,
            shell=False
        )
        log("Clone complete.")

    # ---------------------------------------------------------
    # Commit & push student's results
    # ---------------------------------------------------------

    def push_results(self, student_name):
        """
        Adds, commits, and pushes the student's folder.
        """
        student_path = os.path.join(self.repo_path, student_name)

        if not os.path.exists(student_path):
            log(f"[GIT ERROR] No folder found for {student_name}")
            return

        # Stage the student folder
        self._git(["add", student_name])

        # Commit
        commit_msg = f"Results for {student_name}"
        self._git(["commit", "-m", commit_msg])

        # Push
        self._git(["push"])
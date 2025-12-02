import subprocess
import os
import shlex
from eval_core.utils import log

class SandboxResult:
    def __init__(self, stdout, stderr, exit_code):
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code


class SandboxRunner:
    #regex security
    SAFE_REGEX = r"^[a-zA-Z0-9_\-\.\/]+$"

    def __init__(self, timeout=2):
        self.timeout = timeout

    # -----------------------------------------
    # SAFETY: validate file path
    # -----------------------------------------

    def validate_path(self, file):
        """
        Minimal path validation:
        - only alphanumeric / . / _ / -
        - absolute path check
        - no traversal
        """
        file = os.path.abspath(file)
        root = os.getcwd()

        if not file.startswith(root):
            raise PermissionError(f"[SECURITY] Attempt to escape working directory: {file}")

        if not os.path.exists(file):
            raise FileNotFoundError(f"[SECURITY] File not found: {file}")

        return file
        #TODO: add strict regex, add chroot

    # -----------------------------------------
    # Python Runner
    # -----------------------------------------


    def _run_python(self, file_path, input_data):
        if input_data is None:
            input_data = ""

        cmd = ["python3", file_path]

        try:
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout, stderr = process.communicate(
                input_data, timeout=self.timeout
            )

            return SandboxResult(stdout, stderr, process.returncode)
        except subprocess.TimeoutExpired:
            process.kill()
            return SandboxResult("", "Timeout", 1)

        except Exception as e:
            return SandboxResult("", str(e), 1)

    # -----------------------------------------
    # MAIN SANDBOX EXECUTION
    # -----------------------------------------

    def run(self, file_path, language, input_data):
        try:
            if language == "python":
                return self._run_python(file_path, input_data)
            else:
                raise ValueError(f"Language not supported: {language}")
        except Exception as e:
            log(f"[SANDBOX ERROR] {e}")
            return SandboxResult("", str(e), 1)

    #TODO: add memory quota (linux only), add cpu limit, add audit stderr to detect file
    #add other langage runner
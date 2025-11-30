import subprocess
import os
import shlex
from eval_core.utils import log

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
        return subprocess.run(
            ["python3", file_path],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=self.timeout,
            env={},                   # no env vars
            shell=False               # NEVER use shell=True
        )

    # -----------------------------------------
    # C Runner
    # -----------------------------------------

    def _run_c(self, file_path, input_data):
        """
        Expects a compiled C executable.
        (Compilation step could be added later)
        """
        return subprocess.run(
            [file_path],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=self.timeout,
            env={},
            shell=False
        )

    # -----------------------------------------
    # Java Runner
    # -----------------------------------------

    def _run_java(self, class_name, input_data):
        return subprocess.run(
            ["java", class_name],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=self.timeout,
            env={},
            shell=False
        )

    # -----------------------------------------
    # MAIN SANDBOX EXECUTION
    # -----------------------------------------

    def run(self, file_path, language, input_data=""):
        """
        Execute student code safely.
        Returns dict: { stdout, stderr, error }
        """

        try:
            safe_file = self.validate_path(file_path)

            if language == "python":
                result = self._run_python(safe_file, input_data)

            elif language == "c":
                # TODO: Add auto-compilation step if needed
                result = self._run_c(safe_file, input_data)

            elif language == "java":
                # Java needs class name, not file --> careful with this
                #TODO: add auto-compilation

                # Class name extraction with security check
                filename = os.path.basename(safe_file)

                if not filename.endswith(".java"):
                    raise ValueError("[SECURITY] Java file must end with .java")

                class_name = filename[:-5]  # remove .java

                # SECURITY: Java identifiers rules
                if not class_name.isidentifier():
                    raise ValueError(f"[SECURITY] Invalid Java class name: {class_name}")

                result = self._run_java(class_name, input_data)

            else:
                raise ValueError(f"[ERROR] Unknown language: {language}")

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "error": bool(result.stderr)
            }

        except subprocess.TimeoutExpired:
            log(f"[TIMEOUT] {file_path}")
            return {
                "stdout": "",
                "stderr": "Timeout",
                "error": True
            }

        except Exception as e:
            # catch ANY other runtime/security error
            log(f"[SANDBOX ERROR] {e}")
            return {
                "stdout": "",
                "stderr": str(e),
                "error": True
            }
        #TODO: add memory quota (linux only), add cpu limit, add audit stderr to detect file access
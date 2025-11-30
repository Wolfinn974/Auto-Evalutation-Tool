import time
import random
from eval_core.utils import log

class CooldownManager:

    def __init__(self, config):
        self.base_penalty = config["penalty_start_seconds"]
        self.increment = config["penalty_increment_seconds"]
        self.mode = config.get("penalty_mode", "linear")  # optional config (linear/exponential)

    # ---------------------------------------------------------
    # CALCULATE PENALTY
    # ---------------------------------------------------------

    def _calculate_penalty(self, attempt):
        """
        Returns cooldown in seconds.
        attempt = number of failed attempts so far.
        """

        if self.mode == "linear":
            return self.base_penalty + (attempt - 1) * self.increment

        elif self.mode == "exponential":
            return self.base_penalty * (2 ** (attempt - 1))

        # fallback fail-safe
        return self.base_penalty

    # ---------------------------------------------------------
    # APPLY COOLDOWN
    # ---------------------------------------------------------

    def apply_penalty(self, attempt):
        """
        Waits for the calculated cooldown time.
        """
        penalty = self._calculate_penalty(attempt)

        log(f"Applying cooldown: {penalty}s (attempt {attempt})")

        print(f"\n⏳ Please wait {penalty} seconds before trying again...\n")

        # SAFETY: small sleep chunks (prevents engine freeze)
        remaining = penalty
        while remaining > 0:
            chunk = min(5, remaining)
            time.sleep(chunk)
            remaining -= chunk

    # ---------------------------------------------------------
    # ROAST PICKER
    # ---------------------------------------------------------

    def roast(self, error_type, roast_bank, exo_name=None):
        """
        Picks a roast from:
        - specific exercise (if exists)
        - or global roast category
        - or fallback random
        """

        # 1 — Specific roast for this exercise
        if exo_name and exo_name in roast_bank:
            return random.choice(roast_bank[exo_name])

        # 2 — Global category (wrong_output, wrong_filename, runtime_error, qcm, etc.)
        if "global" in roast_bank and error_type in roast_bank["global"]:
            return random.choice(roast_bank["global"][error_type])

        if error_type in roast_bank:
            return random.choice(roast_bank[error_type])

        # 3 — Fallback roast (very rare)
        return "Hmm… choix interessant. Incorrect, mais interessant."
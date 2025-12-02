import random
from eval_core.utils import log

class QCMEngine:

#todo:
#add security in path and regex

    def __init__(self, qcm_bank, config):
        self.qcm_bank = qcm_bank["questions"]
        self.config = config
        self.selected_questions = []
        self.score = 0

    # -----------------------------------
    # SELECT QUESTIONS
    # -----------------------------------

    def pick_questions(self):
        q_count = self.config["qcm_count"]
        self.selected_questions = random.sample(self.qcm_bank, q_count)
        log(f"QCM: Selected {q_count} questions.")
        #TODO:add level mode gamble add select by tags

    # -----------------------------------
    # ASK QUESTIONS
    # -----------------------------------

    def _ask_question(self, q):
        print("\n-------------------------------------------")
        print(f"Question: {q['question']}")

        # Shuffle choices to avoid memorisation
        choices = list(q["choices"])
        random.shuffle(choices)

        for choice in choices:
            print(choice)

        # Input loop
        answer = input("\nYour answer (A/B/C/D…): ").strip().upper()
        #TODO: replace by silent auto eval mode add roasting for bad answers

        # Extract the letter from "A: text"
        correct_letter = q["answer"].upper().strip()

        if answer == correct_letter:
            log(f"QCM correct answer for {q['id']}.")
            pts = q.get("points", 0)
            return pts
        else:
            log(f"QCM wrong answer for {q['id']}. Expected {correct_letter}, got {answer}.")
            return 0

    # -----------------------------------
    # RUN THE WHOLE QCM
    # -----------------------------------

    def run(self):
        #TODO: add a final recap add log by question in the individual file
        if not self.selected_questions:
            raise Exception("QCM questions not selected. Call pick_questions() first.")

        total = 0
        question_number = 1

        print("\n========== QCM SECTION ==========")
        print(f"You will answer {len(self.selected_questions)} questions.\n")

        for q in self.selected_questions:
            print(f"--- Question {question_number} ---")
            gained = self._ask_question(q)
            total += gained
            question_number += 1

        self.score = total
        log(f"QCM finished with score {self.score}.")

        return self.score
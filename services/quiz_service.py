import json
import re
from markdown import markdown
from flask import session
from utils.markdown_utils import markdown_to_list

class QuizService:
    def __init__(self, ai_model):
        self.ai_model = ai_model

    def create_quiz(self, language, questions, choices):
        prompt = f"Hello, please prepare a quick quiz on this programming language: {language} and prepare {questions} number of questions and for each of them keep {choices} number of choices."
        response = self.ai_model.generate_content(prompt)

        quiz_content = re.search(r'{.*}', response, re.DOTALL).group()
        quiz_content = json.loads(quiz_content)
        session['response'] = quiz_content
        return quiz_content

    def evaluate_quiz(self, given_answers):
        score = 0
        actual_answers = [q["answer"].strip() for q in session['response']["questions"]]
        for i in range(len(actual_answers)):
            if actual_answers[i] == given_answers[i].strip() or actual_answers[i][0].lower() == given_answers[i][0].lower():
                score += 1
        return score, actual_answers, given_answers

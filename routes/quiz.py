from flask import Blueprint, render_template, request
from services.quiz_service import QuizService
from services.recommendation_service import *

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route("/quiz_interface")
def quiz_interface():
    return render_template("home.html")


@quiz_bp.route("/quiz", methods=["GET", "POST"])
def quiz():
    if (request.method == "POST"):
        print(request.form)
        language = request.form["language"]
        questions = request.form["ques"]
        choices = request.form["choices"]
        #difficulty = request.form["diff"]
        prompt = f"Hello, please prepare a quick quiz on this programming language: {language} and prepare {questions} number of questions and for each of them keep {choices} number of choices, reply in the form of an object, make sure the response object contains topic, questions array containing question, choices and it's answer,print them in json format"

        response = model.generate_content(prompt)
        # ic(response)

        quiz_content= re.search(r'{.*}',response.parts[0].text, re.DOTALL).group()
        # print(response['choices'][0]['message']['content'])
        # quiz_content = response['choices'][0]['message']['content']
        #print(quiz_content)

        # Convert the content string to a dictionary
        # ic(response.parts[0].text[7:])
        quiz_content = json.loads(quiz_content)
        
        session['response'] = quiz_content
        # app.secret_key = os.environ.get("SECRET_KEY")

        return render_template("quiz.html", quiz_content=quiz_content)
    
    if request.method == "GET":
        score = 0
        actual_answers = []
        given_answers = list(request.args.values()) or []
        res = session.get('response', None)
        for answer in res["questions"]:
            actual_answers.append(answer["answer"])
        if len(given_answers)!= 0:
            ic(len(actual_answers), len(given_answers))
            for i in range(len(actual_answers)):
                actual_answers[i] = actual_answers[i].strip()
                given_answers[i] = given_answers[i].strip()
                if actual_answers[i] == given_answers[i] or actual_answers[i][0].lower() == given_answers[i][0].lower():
                    score=score+1
        return render_template("score.html", actual_answers=actual_answers, given_answers=given_answers, score=score)

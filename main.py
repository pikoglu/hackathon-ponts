from flask import Flask
from flask import render_template, request
from src.utils.ask_question_to_pdf import gpt3_completion, ask_question_to_pdf

app = Flask(__name__)

# Global variable to store conversation history
conversation_history = []


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/prompt", methods=["POST"])
def prompt():
    global conversation_history
    question = request.form["prompt"]
    full_question = "\n".join(conversation_history) + "\n" + question
    reponse = gpt3_completion(full_question)
    conversation_history.append(question)
    conversation_history.append(reponse)
    return {"answer": reponse}


@app.route("/question", methods=["GET"])
def question():
    question = "Genere en francais une seule question pertinente sur le texte"
    user_answer = ask_question_to_pdf(question)
    print(user_answer)
    return {"answer": user_answer}


@app.route("/answer", methods=["POST"])
def answer():
    question = request.form["question"]
    user_answer = request.form["prompt"]
    reponse = is_answer_correct(question, user_answer)
    return {"answer": reponse}


def is_answer_correct(question, user_answer):
    evaluation_prompt = f"La question portant sur le texte était : {question}\n La réponse apportée : {user_answer}\n Si la réponse n'est pas correcte dis moi FAUX et donne moi une explication concise de la réponse correcte. \n Si la réponse est correcte dis moi VRAI et felicite moi "
    response = ask_question_to_pdf(evaluation_prompt)
    return response

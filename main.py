from flask import Flask
from flask import render_template, request
from src.utils.ask_question_to_pdf import gpt3_completion,ask_question_to_pdf
app = Flask(__name__)



global souvenir="Voici ce sur quoi nos conversations précédentes ont porté :"

@app.route("/")
def hello_world():
     return render_template('index.html')


@app.route("/prompt", methods=['POST'])
def prompt():
    question = request.form["prompt"]
    reponse = gpt3_completion(question)
    return {'answer':reponse}

@app.route("/question", methods=['GET'])
def question():
    question = "Genere en francais une seule question pertinente sur le texte"
    user_answer = ask_question_to_pdf(question)
    souvenir= souvenir + "\n Tu m'as posé cette question :"+ question 
    return {'answer':user_answer}

@app.route("/answer", methods=['POST'])
def answer():
    question = request.form["question"]
    user_answer = request.form["prompt"]
    souvenir= souvenir + "\n J'ai répondu cela à ta question précédente :"+ reponse 
    reponse= is_answer_correct(question, user_answer)
    return {'answer':reponse}

def is_answer_correct(question, user_answer):
    evaluation_prompt = f"J'avais la question suivante portant sur le texte : {question}\n Ma réponse est : {user_answer}\n Ma réponse est elle correcte ? Si OUI dis moi VRAI, SI NON explique moi pour que je comprenne mieux."
    response=ask_question_to_pdf(evaluation_prompt)
    return response
from flask import Flask
from flask import render_template, request
from src.utils.ask_question_to_pdf import gpt3_completion,ask_question_to_pdf
app = Flask(__name__)

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
    question = "Genere une question pertinente sur le texte"
    user_answer = ask_question_to_pdf(question)
    print(user_answer)
    return {'answer':user_answer}

@app.route("/answer", methods=['POST'])
def answer():
    question = request.form["question"]
    user_answer = request.form["prompt"]
    reponse= is_answer_correct(question, user_answer)
    return {'answer':reponse}

def is_answer_correct(question, user_answer):
    evaluation_prompt = f"Question: {question}\n Answer: {user_answer}\n La réponse est-elle correcte ?\n Answer:"
    response=ask_question_to_pdf(evaluation_prompt)
    return response
from flask import Flask, render_template, request, jsonify
from src.utils.ask_question_to_pdf import gpt3_completion, ask_question_to_pdf

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/prompt", methods=['POST'])
def prompt():
    question = request.form["prompt"]
    reponse = gpt3_completion(f"Répondez de manière concise à la question suivante : {question}", max_tokens=30, temperature=0.5)
    return jsonify({'answer': reponse})

@app.route("/question", methods=['GET'])
def question():
    prompt = "Génère une question pertinente basée sur le texte suivant : "
    question = ask_question_to_pdf(prompt, max_tokens=30, temperature=0.5)
    return jsonify({'question': question})

@app.route("/answer", methods=['POST'])
def answer():
    question = request.form["question"]
    user_answer = request.form["prompt"]
    reponse = is_answer_correct(question, user_answer)
    return jsonify({'answer': reponse})


def is_answer_correct(question, user_answer):
    evaluation_prompt = f"La question posée était : '{question}'. La réponse donnée par l'utilisateur est : '{user_answer}'. Cette réponse est-elle correcte ?"
    gpt3_response = ask_question_to_pdf(evaluation_prompt, max_tokens=5, temperature=0.2)

    # Vous pouvez ajouter ici de la logique pour interpréter la réponse de GPT-3
    return gpt3_response

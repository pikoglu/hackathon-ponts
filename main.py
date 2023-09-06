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
    reponse = ask_question_to_pdf(question)
    return {'answer':reponse}

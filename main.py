from flask import Flask
from flask import render_template, request
from src.utils.ask_question_to_pdf import gpt3_completion
app = Flask(__name__)

@app.route("/")
def hello_world():
     return render_template('index.html')

@app.route("/prompt", methods=['POST'])
def prompt():
    question = request.form["prompt"]
    reponse = gpt3_completion(question)
    return {'answer':reponse}

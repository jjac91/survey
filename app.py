from http.client import responses
from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses=[]
@app.route('/')
def index():
    """Returns starting page with survey title and instructions"""
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("start.html",title=title, instructions=instructions)

@app.route('/question/<question_num>')
def quest(question_num):
    "Show page with appropriately numbered question"
    question = satisfaction_survey.questions[int(question_num)]
    choices = question.choices
    return render_template("question.html", question=question ,num=len(responses)+1, choices= choices)
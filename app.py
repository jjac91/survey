from http.client import responses
from flask import Flask, request, render_template,redirect,flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def index():
    """Returns starting page with survey title and instructions"""
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("start.html",title=title, instructions=instructions)

@app.route('/begin', methods = ["POST"])
def begin_survey():
    session['responses'] = []
    return redirect("/question/0")

@app.route('/question/<int:question_num>')
def quest(question_num):
    """Show page with appropriately numbered question"""
    response = session.get('responses')
    
    if (response is None) :
       return redirect("/")
    
    if len(response) == len(satisfaction_survey.questions):
        return redirect("/thanks")

    if len(response) != (question_num):
        flash("Returning you to your question")
        return redirect(f"/question/{len(response)}")

    question = satisfaction_survey.questions[question_num]
    choices =question.choices    
    return render_template("question.html", question=question, choices=choices)

@app.route('/answer', methods=["POST"])
def get_answer():
    """Get response and move to next question"""
    
    survey_answer=request.form["s_question"]
    
    responses = session['responses']
    responses.append(survey_answer)
    session['responses'] = responses
    
    if len(responses) == len(satisfaction_survey.questions):
        return redirect("/thanks")
    else: 
        return redirect(f"/question/{len(responses)}")

@app.route("/thanks")
def thanks():
    """Thank you page for completing the survey"""

    return render_template("/thanks.html")
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from random import randint, choice, sample
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "canilive"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

RESPONSES_KEY = "responses"

@app.route("/")
def home():
    """Opens the Survey"""
    return render_template("home.html")

@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route("/thanks")
def thanks():
    """Thanks user for participating in survey"""
    return render_template("thanks.html")

@app.route("/questions/<int:id>")
def question1(id):
    """Displays the current question"""
    if(id >= len(satisfaction_survey.questions)):
        flash("Redirected to current question.")
        return redirect(f"/questions/{len(responses)}")
    else:
        return render_template("question.html",survey=satisfaction_survey.questions[id])

@app.route("/answer", methods=["POST"])
def answer():
    """Stores an answer in sessions and then presents the next question"""
    choice = request.form["choice"]

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if(len(responses) == len(satisfaction_survey.questions)):
       return redirect("/thanks")
    else:
        return redirect(f"/questions/{len(responses)}")

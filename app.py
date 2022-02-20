from flask import Flask, render_template, request, redirect, flash
from flask import flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config["SECRET_KEY"] = "w57h63ff"
debug = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


responses = []

@app.route("/")
def home_page():
    return render_template("home.html", survey=survey)


@app.route("/questions/<num>")
def question(num):
    index = len(responses) if responses else 0

    if index == len(survey.questions):
        flash("Invalid Page Request!")
        return redirect("/survey_complete")
    elif int(num) != len(responses):
        flash("Invalid Page Request!")
        return redirect(f"/questions/{index}")
    else:
        question = survey.questions[index]
        return render_template("question.html", question=question, index=index)


@app.route("/answers/<num>", methods=["POST"])
def record_answer(num):
    answer = request.form["answer"]
    responses.append(answer)
    next = int(num)+1
    if next < len(survey.questions):
        return redirect(f"/questions/{next}")
    else:
        return redirect("/survey_complete")


@app.route("/survey_complete")
def complete():
    return render_template("survey_complete.html")

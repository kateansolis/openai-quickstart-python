import os

import openai
from flask import Flask, redirect, render_template, request, url_for
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        answer = request.form["answer"]
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=generate_prompt(answer),
            max_tokens=2000,
            top_p=1,
            frequency_penalty=0.67,
            presence_penalty=0
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(answer):
    return format(
        answer.capitalize()
    )

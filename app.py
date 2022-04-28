import os

import openai
from flask import Flask, redirect, render_template, request, url_for
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        question = request.form["answer"]
        response1 = openai.Completion.create(
            engine="text-davinci-002",
            prompt=question,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0)
        response2 = openai.Completion.create(
            engine="text-davinci-002",
            prompt=generate_prompt_step_by_step(question),
            max_tokens=256,
            temperature=0,
            top_p=1,
            frequency_penalty=0.67,
            presence_penalty=0)
        response3 = openai.Answer.create(
            search_model="text-curie-001", 
            model="text-davinci-002", 
            question=question,
            file="file-i1lZjVdoTHP8VJk76kR8aSWe", 
            examples_context="If you’ve received the following error code 0x80190005, we have solutions that may help you to resolve your issue.", 
            examples=[["What is error code 0x80190005", "If you’ve received the following error code 0x80190005, we have solutions that may help you to resolve your issue."]], 
            max_rerank=4,
            max_tokens=256,
            stop=["\n", "<|endoftext|>"]
        )
        score = 0
        text = ""
        if response3 != None:
            document = find_selected_document(response3)
            text = document.text
            score = document.score
        return redirect(url_for("index", result1 =response1.choices[0].text, result2 =response2.choices[0].text, result3 =response3.answers[0] , question = question, search = text, score = score))

    question = request.args.get("question")
    result1 = request.args.get("result1")
    result2 = request.args.get("result2")
    result3 = request.args.get("result3")
    search = request.args.get("search")
    score = request.args.get("score")
    return render_template("index.html", result1=result1, result2=result2, result3=result3, question=question, score=score, search=search)


def generate_prompt_step_by_step(answer):
    return format(
        answer.capitalize() + "\nTell me in step-by-step format:"
    )


def find_selected_document(response):
    documents = response.selected_documents
    largest_score = documents[0]
    for document in documents:
        if document.score > largest_score.score:
            largest_score = document
    return largest_score

@app.route('/summary', methods=("GET", "POST")) 
def summary():
    if request.method == "POST":
        question = request.form["description"]
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=question,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0)
        return redirect(url_for("summary", result =response))
    result = request.args.get("result")
    return render_template("summary.html", result=result)
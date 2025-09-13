from flask import Flask, render_template, request
from agent import ask_agent

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    query = None
    if request.method == "POST":
        query = request.form.get("query")
        if query:
            try:
                answer = ask_agent(query)
            except Exception as e:
                answer = f"Error: {e}"
    return render_template("index.html", answer=answer, query=query)


if __name__ == "__main__":
    app.run(debug=True)

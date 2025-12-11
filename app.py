from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "quiz_secret_key"

# Users (dummy)
users = {"admin": "1234", "kasthuri": "abcd"}

# Quiz questions
quiz = [
    {"question": "What is 2 + 2?", "options": ["2", "3", "4", "5"], "answer": "4"},
    {"question": "Capital of India?", "options": ["Delhi", "Mumbai", "Kolkata", "Chennai"], "answer": "Delhi"},
    {"question": "Which language is used for web apps?", "options": ["Python", "HTML", "C++", "Java"], "answer": "HTML"}
]

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("quiz_page"))
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz_page():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        score = 0
        for i, q in enumerate(quiz):
            if request.form.get(f"question{i}") == q["answer"]:
                score += 1
        return render_template("result.html", score=score, total=len(quiz))
    return render_template("quiz.html", quiz=quiz)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

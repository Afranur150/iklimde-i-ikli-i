from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


# ==========================================
# VERİTABANI
# ==========================================

def get_db():
    return sqlite3.connect("database.db")


def create_database():
    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            carbon REAL,
            quiz_score INTEGER
        )
    """)

    db.commit()
    db.close()


# ==========================================
# ANA SAYFA
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# BİLGİLER SAYFASI
# ==========================================

@app.route("/questions")
def questions():
    return render_template("questions.html")


# ==========================================
# KARBON AYAK İZİ HESAPLAMA
# ==========================================

@app.route("/calculator", methods=["GET", "POST"])
def calculator():

    carbon = None

    if request.method == "POST":

        electricity = float(request.form["electricity"])
        transport = float(request.form["transport"])
        meat = float(request.form["meat"])

        # Basit örnek karbon hesaplama
        carbon = (
            electricity * 0.5
            + transport * 0.2
            + meat * 1.5
        )

        name = request.form["name"]

        db = get_db()

        db.execute(
            "INSERT INTO results (name, carbon, quiz_score) VALUES (?, ?, ?)",
            (name, carbon, 0)
        )

        db.commit()
        db.close()

    return render_template(
        "calculator.html",
        carbon=carbon
    )


# ==========================================
# QUIZ
# ==========================================

@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    score = None

    if request.method == "POST":

        score = 0

        answers = {
            "q1": "b",
            "q2": "a",
            "q3": "c",
            "q4": "b",
            "q5": "a"
        }

        for question, correct_answer in answers.items():

            user_answer = request.form.get(question)

            if user_answer == correct_answer:
                score += 1

    return render_template(
        "quiz.html",
        score=score
    )


# ==========================================
# SONUÇLAR
# ==========================================

@app.route("/results")
def results():

    db = get_db()

    data = db.execute(
        "SELECT * FROM results ORDER BY id DESC"
    ).fetchall()

    db.close()

    return render_template(
        "result.html",
        results=data
    )


# ==========================================
# PROGRAMI BAŞLAT
# ==========================================

if __name__ == "__main__":

    create_database()

    app.run(debug=True)

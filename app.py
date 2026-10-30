
import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/student")
def get_student():
    return jsonify({
        "student_id": "2024-00146",
        "name": "Gwyneth Joy Laud",
        "program": "BSIT",
        "year": 3,
        "section": "B"
    })


@app.route("/hello")
def say_hello():
    name = request.args.get("name", "Student")
    return jsonify({
        "message": f"Hello, {name}!"
    })


@app.route("/skills")
def get_skills():
    return jsonify({
        "student": "Gwyneth Joy Laud",
        "skills": [
            "Python",
            "Flask",
            "HTML",
            "CSS",
            "JavaScript",
            "MySQL"
        ]
    })


@app.route("/students")
def get_students():
    conn = get_db_connection()
    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()
    conn.close()

    return jsonify([dict(student) for student in students])


@app.route("/students/<int:id>")
def get_student_by_id(id):
    conn = get_db_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()
    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


@app.route("/students/section/<string:section>")
def get_students_by_section(section):
    conn = get_db_connection()
    students = conn.execute(
        "SELECT * FROM students WHERE section = ?",
        (section,)
    ).fetchall()
    conn.close()

    return jsonify([dict(student) for student in students])


if __name__ == "__main__":
    app.run(debug=True)

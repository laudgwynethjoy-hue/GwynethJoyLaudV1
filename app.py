
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


# DISPLAY ALL STUDENTS
@app.route("/students", methods=["GET"])
def get_students():
    conn = get_db_connection()
    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()
    conn.close()

    return jsonify([dict(student) for student in students])


# DISPLAY ONE STUDENT
@app.route("/students/<int:id>", methods=["GET"])
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


# DISPLAY STUDENTS BY SECTION
@app.route("/students/section/<string:section>", methods=["GET"])
def get_students_by_section(section):
    conn = get_db_connection()
    students = conn.execute(
        "SELECT * FROM students WHERE section = ?",
        (section,)
    ).fetchall()
    conn.close()

    return jsonify([dict(student) for student in students])


# VALIDATE STUDENT DATA
def validate_student_data(data):
    required_fields = [
        "student_id",
        "name",
        "program",
        "year",
        "section"
    ]

    if not isinstance(data, dict):
        return "Invalid JSON data"

    for field in required_fields:
        if field not in data or str(data[field]).strip() == "":
            return f"{field} is required"

    try:
        year = int(data["year"])
        if year < 1:
            return "Year must be greater than 0"
    except (ValueError, TypeError):
        return "Year must be a valid number"

    return None


# CREATE - ADD STUDENT
@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True)
    error = validate_student_data(data)

    if error:
        return jsonify({"error": error}), 400

    try:
        conn = get_db_connection()

        cursor = conn.execute(
            """INSERT INTO students
            (student_id, name, program, year, section)
            VALUES (?, ?, ?, ?, ?)""",
            (
                data["student_id"].strip(),
                data["name"].strip(),
                data["program"].strip(),
                int(data["year"]),
                data["section"].strip()
            )
        )

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return jsonify({
            "message": "Student added successfully",
            "id": new_id
        }), 201

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500


# READ - GET ONE STUDENT THROUGH API
@app.route("/api/students/<int:id>", methods=["GET"])
def api_get_student(id):
    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# UPDATE - EDIT STUDENT
@app.route("/api/students/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.get_json(silent=True)
    error = validate_student_data(data)

    if error:
        return jsonify({"error": error}), 400

    try:
        conn = get_db_connection()

        existing_student = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (id,)
        ).fetchone()

        if existing_student is None:
            conn.close()
            return jsonify({"error": "Student not found"}), 404

        conn.execute(
            """UPDATE students
            SET student_id = ?, name = ?, program = ?,
                year = ?, section = ?
            WHERE id = ?""",
            (
                data["student_id"].strip(),
                data["name"].strip(),
                data["program"].strip(),
                int(data["year"]),
                data["section"].strip(),
                id
            )
        )

        conn.commit()
        conn.close()

        return jsonify({
            "message": "Student updated successfully"
        })

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500


# DELETE - REMOVE STUDENT
@app.route("/api/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    try:
        conn = get_db_connection()

        cursor = conn.execute(
            "DELETE FROM students WHERE id = ?",
            (id,)
        )

        conn.commit()
        deleted = cursor.rowcount
        conn.close()

        if deleted == 0:
            return jsonify({"error": "Student not found"}), 404

        return jsonify({
            "message": "Student deleted successfully"
        })

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500


# READ-ONLY API FOR CLASSMATES
@app.route("/api/students", methods=["GET"])
def api_students():
    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


if __name__ == "__main__":
    app.run(debug=True)

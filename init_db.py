
import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    name TEXT NOT NULL,
    program TEXT NOT NULL,
    year INTEGER NOT NULL,
    section TEXT NOT NULL
)
""")

cursor.execute("DELETE FROM students")

students = [
    ("24-0087", "KC Jane Marie Ladoing", "BSIT", 3, "B"),
    ("24-00123", "Yvonne Mahilum", "BSIT", 3, "B"),
    ("24-00143", "Kate Ashley Distura", "BSIT", 3, "B"),
    ("24-00319", "Princess Grace Patricio", "BSIT", 3, "C"),
    ("24-00146", "Gwyneth Joy Laud", "BSIT", 3, "B")
]

cursor.executemany("""
INSERT INTO students
(student_id, name, program, year, section)
VALUES (?, ?, ?, ?, ?)
""", students)

conn.commit()
conn.close()

print("Database created successfully.")

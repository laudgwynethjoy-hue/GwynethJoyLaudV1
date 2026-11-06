import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Drop table to apply the updated schema cleanly
cursor.execute("DROP TABLE IF EXISTS students")

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    name TEXT NOT NULL,
    program TEXT NOT NULL,
    year INTEGER NOT NULL,
    section TEXT NOT NULL,
    source TEXT DEFAULT 'Local'
)
""")

students = [
    ("24-0087", "KC Jane Marie Ladoing", "BSIT", 3, "B", "Local"),
    ("24-00123", "Yvonne Mahilum", "BSIT", 3, "B", "Local"),
    ("24-00143", "Kate Ashley Distura", "BSIT", 3, "B", "Local"),
    ("24-00319", "Princess Grace Patricio", "BSIT", 3, "C", "Local"),
    ("24-00146", "Gwyneth Joy Laud", "BSIT", 3, "B", "Local")
]

cursor.executemany("""
INSERT INTO students
(student_id, name, program, year, section, source)
VALUES (?, ?, ?, ?, ?, ?)
""", students)

conn.commit()
conn.close()

print("Database created successfully with 'source' column.")
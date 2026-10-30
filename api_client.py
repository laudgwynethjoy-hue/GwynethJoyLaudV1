python -m pip install -r requirements.txtfrom flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Home Route - Display the Web Interface
@app.route('/')
def home():
    return render_template('index.html')


# Student API Endpoint
@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "2026-00123",
        "name": "Juan Dela Cruz",
        "program": "BSIT",
        "year": 1,
        "section": "A"
    })


# Hello API Endpoint
@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Hello, {name}!"
    })


# Skills API Endpoint
@app.route('/skills')
def get_skills():
    return jsonify({
        "skills": [
            "Python",
            "Flask",
            "API Development"
        ]
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

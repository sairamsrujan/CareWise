from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime
import webbrowser
import threading

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("symptom_history.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptoms TEXT,
            analysis TEXT,
            urgency TEXT,
            timestamp TEXT
        )
        """
    )
    conn.commit()
    conn.close()

# Save data to database
@app.route("/save", methods=["POST"])
def save_to_db():
    data = request.json
    symptoms = data.get("symptoms")
    analysis = data.get("analysis")
    urgency = data.get("urgency")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("symptom_history.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history (symptoms, analysis, urgency, timestamp) VALUES (?, ?, ?, ?)",
        (symptoms, analysis, urgency, timestamp),
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "success"})

# Retrieve data from database
@app.route("/history", methods=["GET"])
def get_history():
    conn = sqlite3.connect("symptom_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history ORDER BY timestamp DESC")
    history = cursor.fetchall()
    conn.close()

    return jsonify(history)

# Serve the homepage
@app.route("/")
def home():
    return render_template("index.html")

# Serve the symptom checker page
@app.route("/symptom_checker")
def symptom_checker():
    return render_template("symptom_checker.html")

# Serve the about page
@app.route("/about")
def about():
    return render_template("about.html")

# Function to open the browser
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    init_db()
    # Open the browser after a short delay
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
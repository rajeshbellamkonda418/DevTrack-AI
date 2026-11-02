import os
import sqlite3
from pathlib import Path

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from ml.model import recommend_jobs
from ml.resume_analyzer import analyze_resume_for_role, extract_text_from_file
from ml.job_search import search_role_jobs

BASE_DIR = Path(__file__).resolve().parent

env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path, override=False)

app = Flask(__name__)
DB_ERRORS = (Error, sqlite3.Error)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


class SQLiteCursor:
    def __init__(self, cursor, dictionary=False):
        self.cursor = cursor
        self.dictionary = dictionary

    def execute(self, query, params=None):
        query = query.replace("%s", "?")
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        return self

    def fetchall(self):
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows] if self.dictionary else rows

    @property
    def lastrowid(self):
        return self.cursor.lastrowid

    @property
    def rowcount(self):
        return self.cursor.rowcount

    def close(self):
        self.cursor.close()


class SQLiteConnection:
    def __init__(self, connection):
        self.connection = connection

    def cursor(self, dictionary=False):
        return SQLiteCursor(self.connection.cursor(), dictionary=dictionary)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()


def get_db():
    if os.getenv("DB_BACKEND", "mysql").lower() == "sqlite":
        database_path = Path(
            os.getenv("SQLITE_PATH", str(BASE_DIR / "database" / "applications.sqlite3"))
        )
        database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(
            database_path,
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        connection.row_factory = sqlite3.Row
        connection.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company VARCHAR(120) NOT NULL,
                role VARCHAR(120) NOT NULL,
                status TEXT NOT NULL DEFAULT 'Applied'
                    CHECK (status IN ('Applied', 'Interview', 'Selected', 'Rejected')),
                skills TEXT,
                applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        return SQLiteConnection(connection)

    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, company, role, status, skills, applied_date
            FROM applications
            ORDER BY id DESC
        """)
        jobs = cursor.fetchall()

        cursor.close()
        conn.close()

        for job in jobs:
            if job["applied_date"]:
                job["applied_date"] = job["applied_date"].isoformat()

        return jsonify(jobs)

    except DB_ERRORS as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/jobs", methods=["POST"])
def add_job():
    data = request.get_json(silent=True) or {}

    company = (data.get("company") or "").strip()
    role = (data.get("role") or "").strip()
    status = (data.get("status") or "Applied").strip()
    skills = (data.get("skills") or "").strip()

    if not company or not role:
        return jsonify({"error": "Company and role are required"}), 400

    if status not in ["Applied", "Interview", "Selected", "Rejected"]:
        return jsonify({"error": "Invalid status"}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO applications
            (company, role, status, skills)
            VALUES (%s, %s, %s, %s)
            """,
            (company, role, status, skills)
        )

        conn.commit()
        new_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Application added successfully",
            "id": new_id
        }), 201

    except DB_ERRORS as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/jobs/<int:job_id>", methods=["PUT"])
def update_job(job_id):
    data = request.get_json(silent=True) or {}
    status = (data.get("status") or "").strip()

    if status not in ["Applied", "Interview", "Selected", "Rejected"]:
        return jsonify({"error": "Invalid status"}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE applications SET status=%s WHERE id=%s",
            (status, job_id)
        )

        conn.commit()
        changed = cursor.rowcount

        cursor.close()
        conn.close()

        if not changed:
            return jsonify({"error": "Application not found"}), 404

        return jsonify({"message": "Status updated successfully"})

    except DB_ERRORS as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM applications WHERE id=%s",
            (job_id,)
        )

        conn.commit()
        changed = cursor.rowcount

        cursor.close()
        conn.close()

        if not changed:
            return jsonify({"error": "Application not found"}), 404

        return jsonify({"message": "Application deleted"})

    except DB_ERRORS as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.get_json(silent=True) or {}

    skills = (data.get("skills") or "").strip()
    if not skills:
        return jsonify({"error": "Enter your skills"}), 400

    recommendations = recommend_jobs(skills)

    return jsonify({
        "recommendations": recommendations
    })


@app.route("/api/analyze-resume", methods=["POST"])
def analyze_resume():
    try:
        target_role = ""
        resume_text = ""

        if "resume" in request.files:
            file = request.files["resume"]
            if not file or not file.filename:
                return jsonify({"error": "No resume file selected"}), 400

            target_role = (request.form.get("role") or "").strip()
            resume_text = extract_text_from_file(file.stream, file.filename)
        else:
            data = request.get_json(silent=True) or {}
            target_role = (data.get("role") or "").strip()
            resume_text = (data.get("resume_text") or "").strip()

        if not target_role:
            return jsonify({"error": "Target role is required for resume analysis"}), 400

        if not resume_text:
            return jsonify({"error": "Please provide a resume file (PDF, DOCX, TXT) or paste resume text"}), 400

        analysis = analyze_resume_for_role(resume_text, target_role)
        return jsonify(analysis)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to analyze resume: {str(e)}"}), 500


@app.route("/api/search-jobs", methods=["GET", "POST"])
def search_jobs():
    try:
        if request.method == "POST":
            data = request.get_json(silent=True) or {}
            role = (data.get("role") or "").strip()
            location = (data.get("location") or "Remote").strip()
            platform = (data.get("platform") or "all").strip().lower()
        else:
            role = (request.args.get("role") or "").strip()
            location = (request.args.get("location") or "Remote").strip()
            platform = (request.args.get("platform") or "all").strip().lower()

        if not role:
            return jsonify({"error": "Role is required for job search"}), 400

        results = search_role_jobs(role=role, location=location, platform=platform)
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": f"Failed to search jobs: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)

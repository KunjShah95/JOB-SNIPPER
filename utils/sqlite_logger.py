import sqlite3
import datetime
import logging
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@contextmanager
def get_db_connection(db_path="history.db"):
    """Context manager for database connections"""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def init_db(db_path="history.db"):
    """Initialize the database with a more comprehensive schema"""
    try:
        with get_db_connection(db_path) as conn:
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS resume_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                name TEXT,
                skills TEXT,
                education TEXT,
                experience TEXT,
                match_percent INTEGER,
                job_title TEXT,
                feedback_summary TEXT,
                suggested_jobs TEXT
            )""")
            
            # Create interactions table
            c.execute("""CREATE TABLE IF NOT EXISTS agent_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                agent_name TEXT,
                action TEXT,
                input_data TEXT,
                output_data TEXT
            )""")
            
            conn.commit()
            logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        raise

def save_to_db(parsed_data, match_result, db_path="history.db"):
    """Save resume analysis results to database with improved error handling"""
    try:
        with get_db_connection(db_path) as conn:
            c = conn.cursor()

            # Handle missing fields with defaults
            name = parsed_data.get("name", "Unknown") if parsed_data else "Unknown"
            skills = parsed_data.get("skills", []) if parsed_data else []
            skills_str = ",".join(skills) if isinstance(skills, list) else str(skills)
            education = parsed_data.get("education", "Unknown") if parsed_data else "Unknown"
            experience = parsed_data.get("experience", "Unknown") if parsed_data else "Unknown"

            # Handle match result with defaults
            match_percent = 0
            job_title = ""
            feedback_summary = ""
            suggested_jobs = ""
            
            if isinstance(match_result, dict):
                match_percent = match_result.get("match_percent", 0)
                job_title = match_result.get("job_title", "")
                feedback_summary = match_result.get("feedback_summary", "")
                suggested_jobs = ",".join(match_result.get("job_roles", []))

            c.execute("""
                INSERT INTO resume_logs 
                (timestamp, name, skills, education, experience, match_percent, job_title, feedback_summary, suggested_jobs) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.datetime.now().isoformat(),
                name,
                skills_str,
                education,
                experience,
                match_percent,
                job_title,
                feedback_summary,
                suggested_jobs,
            ))
            conn.commit()
            logger.info("Data saved to database successfully")
    except Exception as e:
        logger.error(f"Error saving to database: {e}")
        raise

def get_history(limit=10, db_path="history.db"):
    """Retrieve resume analysis history with improved error handling"""
    try:
        with get_db_connection(db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM resume_logs ORDER BY id DESC LIMIT ?", (limit,))
            rows = c.fetchall()
            return rows
    except Exception as e:
        logger.error(f"Error retrieving history: {e}")
        return []

def get_resume_details(resume_id, db_path="history.db"):
    """Get detailed information for a specific resume analysis"""
    try:
        with get_db_connection(db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM resume_logs WHERE id = ?", (resume_id,))
            row = c.fetchone()

            if row:
                columns = [
                    "id", "timestamp", "name", "skills", "education",
                    "experience", "match_percent", "job_title", 
                    "feedback_summary", "suggested_jobs"
                ]
                return dict(zip(columns, row))
            return None
    except Exception as e:
        logger.error(f"Error retrieving resume details: {e}")
        return None

def log_interaction(agent_name, action, input_data, output_data, db_path="history.db"):
    """Log agent interactions for debugging and analysis"""
    try:
        with get_db_connection(db_path) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO agent_interactions 
                (timestamp, agent_name, action, input_data, output_data) 
                VALUES (?, ?, ?, ?, ?)
            """, (
                datetime.datetime.now().isoformat(),
                agent_name,
                action,
                str(input_data)[:5000],  # Limit input data length
                str(output_data)[:5000],  # Limit output data length
            ))
            conn.commit()
    except Exception as e:
        logger.error(f"Error logging interaction: {e}")

class SQLiteLogger:
    """SQLiteLogger class to provide compatibility with existing app.py imports"""

    def __init__(self, db_path="history.db"):
        """Initialize SQLiteLogger with database path"""
        self.db_path = db_path
        init_db(self.db_path)

    def log_analysis(self, analysis_data, filename):
        """Log resume analysis data"""
        try:
            parsed_data = analysis_data.get("parsed_data", {}) if analysis_data else {}
            
            match_result = {
                "match_percent": analysis_data.get("overall_score", 0) if analysis_data else 0,
                "job_title": analysis_data.get("target_job", "") if analysis_data else "",
                "feedback_summary": ", ".join(analysis_data.get("recommendations", [])) if analysis_data else "",
                "job_roles": analysis_data.get("job_suggestions", []) if analysis_data else [],
            }

            save_to_db(parsed_data, match_result, self.db_path)
            logger.info(f"Analysis logged for file: {filename}")

        except Exception as e:
            logger.error(f"Error in log_analysis: {e}")

    def get_history(self, limit=10):
        """Get analysis history"""
        return get_history(limit, self.db_path)

    def get_resume_details(self, resume_id):
        """Get specific resume details"""
        return get_resume_details(resume_id, self.db_path)

    def log_interaction(self, agent_name, action, input_data, output_data):
        """Log agent interactions"""
        return log_interaction(agent_name, action, input_data, output_data, self.db_path)
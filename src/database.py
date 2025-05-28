import sqlite3
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
from .config import get_config

class Database:
    def __init__(self):
        self.config = get_config()
        self._init_db()

    def _init_db(self):
        """Initialize database with required tables."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create indexes for frequently queried fields
            cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
            CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(date);
            CREATE INDEX IF NOT EXISTS idx_messages_sender_receiver ON messages(sender_id, receiver_id);
            CREATE INDEX IF NOT EXISTS idx_prescriptions_patient ON prescriptions(patient_id);
            ''')
            
            conn.commit()

    @contextmanager
    def get_connection(self):
        """Get a database connection with proper configuration."""
        conn = sqlite3.connect(self.config.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a query and return results as a list of dictionaries."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an update query and return the number of affected rows."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email."""
        query = "SELECT * FROM users WHERE email = ?"
        results = self.execute_query(query, (email,))
        return results[0] if results else None

    def get_user_appointments(self, user_id: int, role: str) -> List[Dict[str, Any]]:
        """Get appointments for a user based on their role."""
        if role == 'doctor':
            query = "SELECT * FROM appointments WHERE doctor_id = ? ORDER BY date DESC"
        else:
            query = "SELECT * FROM appointments WHERE patient_id = ? ORDER BY date DESC"
        return self.execute_query(query, (user_id,))

    def get_user_prescriptions(self, user_id: int, role: str) -> List[Dict[str, Any]]:
        """Get prescriptions for a user based on their role."""
        if role == 'doctor':
            query = "SELECT * FROM prescriptions WHERE doctor_id = ? ORDER BY date DESC"
        else:
            query = "SELECT * FROM prescriptions WHERE patient_id = ? ORDER BY date DESC"
        return self.execute_query(query, (user_id,))

    def get_chat_messages(self, user1_id: int, user2_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get chat messages between two users."""
        query = """
        SELECT * FROM messages 
        WHERE (sender_id = ? AND receiver_id = ?) 
           OR (sender_id = ? AND receiver_id = ?)
        ORDER BY created_at DESC
        LIMIT ?
        """
        return self.execute_query(query, (user1_id, user2_id, user2_id, user1_id, limit))

    def add_message(self, sender_id: int, receiver_id: int, subject: str, content: str) -> int:
        """Add a new message to the database."""
        query = """
        INSERT INTO messages (sender_id, receiver_id, subject, content)
        VALUES (?, ?, ?, ?)
        """
        return self.execute_update(query, (sender_id, receiver_id, subject, content))

    def mark_messages_as_read(self, sender_id: int, receiver_id: int) -> int:
        """Mark messages as read."""
        query = """
        UPDATE messages 
        SET is_read = 1 
        WHERE sender_id = ? AND receiver_id = ? AND is_read = 0
        """
        return self.execute_update(query, (sender_id, receiver_id))

# Create a singleton instance
db = Database() 
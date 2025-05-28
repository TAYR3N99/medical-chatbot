import os
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from .config import get_config
from .middleware import sanitize_input

config = get_config()

def generate_password_hash(password: str) -> str:
    """Generate a secure password hash."""
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    return salt.hex() + key.hex()

def verify_password_hash(stored_hash: str, password: str) -> bool:
    """Verify a password against its hash."""
    salt = bytes.fromhex(stored_hash[:64])
    stored_key = stored_hash[64:]
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    return key.hex() == stored_key

def format_datetime(dt: datetime) -> str:
    """Format datetime for display."""
    return dt.strftime('%Y-%m-%d %H:%M')

def parse_datetime(dt_str: str) -> Optional[datetime]:
    """Parse datetime string."""
    try:
        return datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
    except ValueError:
        return None

def get_time_slots(start_time: str, end_time: str, duration: int = 30) -> list:
    """Generate time slots for appointments."""
    start = datetime.strptime(start_time, '%H:%M')
    end = datetime.strptime(end_time, '%H:%M')
    slots = []
    
    current = start
    while current < end:
        slots.append(current.strftime('%H:%M'))
        current += timedelta(minutes=duration)
    
    return slots

def validate_appointment_time(appointment_time: str, doctor_id: int, date: str) -> bool:
    """Validate if appointment time is available."""
    # This would typically check against existing appointments in the database
    # For now, return True as a placeholder
    return True

def format_prescription(medications: list) -> str:
    """Format prescription medications for display."""
    if not medications:
        return "No medications prescribed"
    
    formatted = []
    for med in medications:
        formatted.append(f"• {med['name']}: {med['dosage']} - {med['instructions']}")
    
    return "\n".join(formatted)

def sanitize_user_data(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize user input data."""
    sanitized = {}
    for key, value in user_data.items():
        if isinstance(value, str):
            sanitized[key] = sanitize_input(value)
        else:
            sanitized[key] = value
    return sanitized

def get_file_extension(filename: str) -> str:
    """Get file extension from filename."""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def is_valid_file_size(file_size: int) -> bool:
    """Check if file size is within limits."""
    return file_size <= config.MAX_CONTENT_LENGTH

def generate_unique_filename(filename: str) -> str:
    """Generate a unique filename for uploads."""
    ext = get_file_extension(filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{timestamp}_{hashlib.md5(filename.encode()).hexdigest()[:8]}.{ext}"

def format_error_message(error: str) -> Dict[str, str]:
    """Format error message for API response."""
    return {
        'error': error,
        'timestamp': datetime.now().isoformat()
    } 
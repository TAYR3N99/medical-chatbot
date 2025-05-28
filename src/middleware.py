from functools import wraps
from flask import request, jsonify, current_app
import time
from collections import defaultdict
import re
from .config import get_config

# Rate limiting storage
request_history = defaultdict(list)
config = get_config()

def rate_limit(f):
    """Rate limiting decorator."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not config.DEBUG:  # Skip rate limiting in debug mode
            ip = request.remote_addr
            now = time.time()
            
            # Clean old requests
            request_history[ip] = [t for t in request_history[ip] if now - t < 3600]
            
            # Check rate limit
            if len(request_history[ip]) >= 50:  # 50 requests per hour
                return jsonify({
                    'error': 'Rate limit exceeded. Please try again later.'
                }), 429
            
            request_history[ip].append(now)
        
        return f(*args, **kwargs)
    return decorated_function

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent XSS attacks."""
    if not text:
        return text
    
    # Remove potentially dangerous HTML tags
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<.*?javascript:.*?>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'<.*?on\w+=.*?>', '', text, flags=re.IGNORECASE)
    
    # Escape HTML special characters
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#x27;')
    
    return text

def validate_file_upload(filename: str) -> bool:
    """Validate file upload."""
    if not filename:
        return False
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def secure_headers(f):
    """Add security headers to responses."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = f(*args, **kwargs)
        
        # Add security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';"
        
        return response
    return decorated_function

def validate_json_request(f):
    """Validate JSON request data."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        try:
            request.get_json()
        except Exception as e:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        return f(*args, **kwargs)
    return decorated_function

def log_request(f):
    """Log request details for debugging."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if config.DEBUG:
            current_app.logger.info(f"Request: {request.method} {request.path}")
            current_app.logger.info(f"Headers: {dict(request.headers)}")
            current_app.logger.info(f"Data: {request.get_data()}")
        
        return f(*args, **kwargs)
    return decorated_function 
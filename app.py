from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from src.prompt import *
import os
import sys
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets
import sqlite3
from functools import wraps

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Flask app instantiation
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generate a random secret key

# API key configuration
OPENAI_API_KEY = "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"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Database setup
def get_db_connection():
    conn = sqlite3.connect('mediconnect.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        phone TEXT,
        role TEXT NOT NULL,
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP
    )
    ''')
    
    # Create doctor_profiles table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS doctor_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        speciality TEXT,
        license_number TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Create password_reset_tokens table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS password_reset_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        token TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on app startup
init_db()

# Login decorator for protected routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Veuillez vous connecter pour accéder à cette page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Connect to Meta Llama 3.3 70B Instruct via OpenRouter
llm = ChatOpenAI(
    temperature=0.4, 
    max_tokens=1000, 
    model_name="meta-llama/llama-3.3-70b-instruct",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=OPENAI_API_KEY
)

# Create prompt for the LLM
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# ✅ Route to render landing page
@app.route("/")
def index():
    return render_template('index.html')

# Authentication routes
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = request.form.get("remember")
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['name'] = f"{user['first_name']} {user['last_name']}"
            
            if remember:
                # Set session to last for 30 days
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=30)
            
            # Update last login time
            conn = get_db_connection()
            conn.execute('UPDATE users SET last_login = ? WHERE id = ?', 
                        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user['id']))
            conn.commit()
            conn.close()
            
            # Redirect based on role
            if user['role'] == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            else:
                return redirect(url_for('patient_dashboard'))
        else:
            flash("Email ou mot de passe incorrect.", "error")
    
    return render_template('auth/login.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        role = request.form.get("role")
        
        # Validation
        if not all([first_name, last_name, email, phone, password, confirm_password, role]):
            flash("Tous les champs sont obligatoires.", "error")
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash("Les mots de passe ne correspondent pas.", "error")
            return render_template('auth/register.html')
        
        conn = get_db_connection()
        existing_user = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        
        if existing_user:
            conn.close()
            flash("Cet email est déjà utilisé.", "error")
            return render_template('auth/register.html')
        
        # Create user
        hashed_password = generate_password_hash(password)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (first_name, last_name, email, phone, password, role) VALUES (?, ?, ?, ?, ?, ?)',
            (first_name, last_name, email, phone, hashed_password, role)
        )
        user_id = cursor.lastrowid
        
        # If doctor, add doctor profile
        if role == 'doctor':
            speciality = request.form.get("speciality")
            license_number = request.form.get("license_number")
            
            if not all([speciality, license_number]):
                conn.rollback()
                conn.close()
                flash("Tous les champs de médecin sont obligatoires.", "error")
                return render_template('auth/register.html')
            
            cursor.execute(
                'INSERT INTO doctor_profiles (user_id, speciality, license_number) VALUES (?, ?, ?)',
                (user_id, speciality, license_number)
            )
        
        conn.commit()
        conn.close()
        
        flash("Compte créé avec succès. Vous pouvez maintenant vous connecter.", "success")
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')

@app.route("/logout")
def logout():
    session.clear()
    flash("Vous avez été déconnecté.", "success")
    return redirect(url_for('login'))

@app.route("/reset-password-request", methods=["GET", "POST"])
def reset_password_request():
    if request.method == "POST":
        email = request.form.get("email")
        
        conn = get_db_connection()
        user = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        
        if user:
            # Generate token
            token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=24)
            
            # Store token in database
            conn.execute('DELETE FROM password_reset_tokens WHERE user_id = ?', (user['id'],))
            conn.execute(
                'INSERT INTO password_reset_tokens (user_id, token, expires_at) VALUES (?, ?, ?)',
                (user['id'], token, expires_at.strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
            
            # Here you would send an email with the reset link
            # For now, we'll just flash the link (in a real app, never do this!)
            reset_url = url_for('reset_password', token=token, _external=True)
            flash(f"Un lien de réinitialisation a été envoyé à votre email. URL: {reset_url}", "success")
            
        else:
            # Don't reveal that the email doesn't exist
            flash("Si votre email existe dans notre base de données, vous recevrez un lien de réinitialisation.", "success")
        
        conn.close()
        return redirect(url_for('login'))
    
    return render_template('auth/reset_password_request.html')

@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    conn = get_db_connection()
    token_data = conn.execute(
        'SELECT user_id, expires_at FROM password_reset_tokens WHERE token = ?', 
        (token,)
    ).fetchone()
    
    if not token_data or datetime.now() > datetime.strptime(token_data['expires_at'], "%Y-%m-%d %H:%M:%S"):
        conn.close()
        flash("Le lien de réinitialisation est invalide ou a expiré.", "error")
        return redirect(url_for('reset_password_request'))
    
    if request.method == "POST":
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if password != confirm_password:
            flash("Les mots de passe ne correspondent pas.", "error")
            return render_template('auth/reset_password.html', token=token)
        
        hashed_password = generate_password_hash(password)
        conn.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, token_data['user_id']))
        conn.execute('DELETE FROM password_reset_tokens WHERE user_id = ?', (token_data['user_id'],))
        conn.commit()
        conn.close()
        
        flash("Votre mot de passe a été réinitialisé. Vous pouvez maintenant vous connecter.", "success")
        return redirect(url_for('login'))
    
    conn.close()
    return render_template('auth/reset_password.html', token=token)

# Dashboard routes (protected)
@app.route("/patient-dashboard")
@login_required
def patient_dashboard():
    if session.get('role') != 'patient':
        flash("Accès non autorisé.", "error")
        return redirect(url_for('index'))
    
    return render_template('patient/dashboard.html')

@app.route("/doctor-dashboard")
@login_required
def doctor_dashboard():
    if session.get('role') != 'doctor':
        flash("Accès non autorisé.", "error")
        return redirect(url_for('index'))
    
    return render_template('doctor/dashboard.html')

@app.route("/chat")
@login_required
def chat_page():
    return render_template('chat.html')

# Update the chat function to work without RAG
@app.route("/get", methods=["GET", "POST"])
@login_required
def chat():
    try:
        user_input = request.form["msg"]
        
        # Make sure the user input is valid
        if not user_input or user_input.strip() == "":
            return "Veuillez poser une question médicale. 🩺"
        
        # Use the LLM directly with an empty context
        response = llm.invoke(prompt.format(input=user_input, context=""))
        
        # The response is now directly from Llama 3.3 70B model
        return response.content
    except Exception as e:
        # Handle any errors
        print(f"Error in chat: {str(e)}")
        return "Désolé, une erreur s'est produite lors du traitement de votre demande. Veuillez réessayer. ⚠️"

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

# Additional pages routes
@app.route("/services")
def services():
    return render_template('services.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # Here you would process the form data, such as sending an email
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        
        # In a real implementation, you would send an email or store in database
        # For now, just flash a success message
        flash("Votre message a été envoyé avec succès. Nous vous répondrons dans les plus brefs délais.", "success")
        return redirect(url_for('contact'))
        
    return render_template('contact.html')

# Run the Flask app
if __name__ == "__main__":
    # Disable Flask's automatic dotenv loading
    sys.argv = ["flask", "run", "--no-load-dotenv", "--host=0.0.0.0", "--port=8080", "--debug"]
    app.run(host="0.0.0.0", port=8080, debug=True, load_dotenv=False)
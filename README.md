# MediConnect - AI-Powered Medical Chatbot

MediConnect is a modern medical platform that connects patients with healthcare professionals. This application features an AI-powered medical chatbot using Meta's Llama 3.3 70B model via OpenRouter.

## Features

### Authentication and User Management
- Secure authentication system with password hashing
- Differentiated registration for doctors and patients
- User profile management
- Password recovery system

### User Interface
- Modern, responsive design
- Dark/light mode support
- Role-based dashboards (doctor/patient)
- Intuitive medical chat interface

### Medical AI Features
- Medical AI chatbot based on advanced LLM models
- Direct interaction with Llama 3.3 70B for medical queries
- User-friendly chat interface

## Technologies Used

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Werkzeug Security
- **AI Integration**: LangChain, OpenRouter
- **LLM Model**: Meta Llama 3.3 70B via OpenRouter

## Installation

### Prerequisites
- Python 3.10+
- pip
- OpenRouter API key

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/your-username/mediconnect.git
cd mediconnect
```

2. Create and activate a virtual environment:
```bash
python -m venv env
# Windows
.\env\Scripts\activate
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API keys in app.py:
```python
# API key configuration
OPENAI_API_KEY = "your-openrouter-api-key"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
```

## Running the Application

To run the application:
```bash
python app.py
```

The application will be accessible at: `http://localhost:8080`

## Project Structure

```
mediconnect/
├── Data/                   # Medical data files
├── env/                    # Virtual environment
├── src/                    # Source code
│   ├── helper.py           # Helper functions
│   ├── prompt.py           # Chatbot prompt templates
│   └── __init__.py         # Python package marker
├── static/                 # Static files (CSS, JS, images)
├── templates/              # HTML templates
│   ├── auth/               # Authentication templates
│   ├── doctor/             # Doctor dashboard templates
│   ├── errors/             # Error page templates
│   ├── patient/            # Patient dashboard templates
│   ├── about.html          # About page
│   ├── base.html           # Base template
│   ├── base_auth.html      # Authentication base template
│   ├── chat.html           # Chat interface
│   ├── contact.html        # Contact page
│   ├── index.html          # Home page
│   └── services.html       # Services page
├── .gitignore              # Git ignore file
├── app.py                  # Main application file
├── LICENSE                 # License file
├── mediconnect.db          # SQLite database
└── requirements.txt        # Python dependencies
```

## Usage Guide

1. **Registration**: Create an account by choosing your role (patient or doctor)
2. **Login**: Sign in with your credentials
3. **Dashboard**: Access your personalized dashboard based on your role
4. **Medical Chat**: Use the AI medical assistant to get information about health or medical questions

## Security

- Passwords hashed with Werkzeug Security
- CSRF protection
- Authentication required for protected routes
- Password recovery tokens with expiration

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributors

- Your contributions are welcome

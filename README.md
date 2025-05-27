# MediConnect - Plateforme Médicale

## Overview
MediConnect is a comprehensive medical platform designed to facilitate communication and management between patients and healthcare providers. It offers features such as user authentication, appointment scheduling, prescription management, real-time chat, and an AI medical assistant.

## Features
- **User Authentication**: Secure login and registration for patients and doctors.
- **Dashboards**: Personalized dashboards for patients and doctors to manage their activities.
- **Appointment Management**: Schedule and manage medical appointments.
- **Prescription Management**: Create and manage prescriptions for patients.
- **Real-time Chat**: Communicate with healthcare providers through a chat interface.
- **AI Medical Assistant**: Get medical advice and information from an AI-powered assistant.
- **Video and Audio Calls**: Conduct video and audio calls with healthcare providers (simulated payment process).

## Setup Instructions
1. **Clone the Repository**: 
   ```bash
   git clone <repository-url>
   cd mediconnect
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access the Application**:
   - Open your web browser and go to `http://localhost:8080`.

## Technologies Used
- **Flask**: Web framework for building the application.
- **SQLite**: Database for storing user and application data.
- **Socket.IO**: For real-time chat functionality.
- **Tailwind CSS**: For styling the user interface.
- **OpenAI API**: For the AI medical assistant.

## License
This project is licensed under the MIT License.

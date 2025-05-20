# MediConnect - Plateforme Médicale

Une plateforme médicale complète permettant la communication entre patients et médecins, avec des fonctionnalités de chat, rendez-vous, prescriptions et assistance médicale IA.

## 🌟 Fonctionnalités

- **Authentification**
  - Inscription/Connexion pour patients et médecins
  - Récupération de mot de passe
  - Profils personnalisés

- **Tableau de bord**
  - Vue spécifique pour patients et médecins
  - Statistiques et notifications
  - Rendez-vous à venir

- **Gestion des rendez-vous**
  - Prise de rendez-vous en ligne
  - Confirmation par email
  - Rappels automatiques

- **Prescriptions**
  - Création de prescriptions par les médecins
  - Demandes de renouvellement
  - Historique des prescriptions

- **Communication**
  - Chat en temps réel entre patients et médecins
  - Notifications de nouveaux messages
  - Assistant médical IA

- **Évaluations**
  - Système de notation des médecins
  - Commentaires et retours
  - Statistiques de satisfaction

## 🚀 Installation

1. Cloner le repository
```bash
git clone https://github.com/votre-username/medical-chatbot-1.git
cd medical-chatbot-1
```

2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement
```bash
# Créer un fichier .env
OPENAI_API_KEY=votre_clé_api
SMTP_USERNAME=votre_email
SMTP_PASSWORD=votre_mot_de_passe
```

5. Initialiser la base de données
```bash
python init_db.py
```

6. Lancer l'application
```bash
python app.py
```

## 💻 Technologies utilisées

- **Backend**
  - Flask
  - SQLite
  - Flask-SocketIO
  - LangChain
  - OpenAI API

- **Frontend**
  - HTML/CSS
  - Tailwind CSS
  - JavaScript
  - Socket.IO

- **Autres**
  - APScheduler pour les tâches planifiées
  - SMTP pour les emails
  - WebSocket pour le chat en temps réel

## 📝 Structure du projet

```
medical-chatbot-1/
├── app.py                 # Application principale
├── requirements.txt       # Dépendances
├── .env                  # Variables d'environnement
├── static/              # Fichiers statiques
├── templates/           # Templates HTML
│   ├── auth/           # Pages d'authentification
│   ├── doctor/         # Interface médecin
│   ├── patient/        # Interface patient
│   └── chat/           # Interface de chat
└── uploads/            # Fichiers uploadés
```

## 🔒 Sécurité

- Authentification sécurisée
- Protection CSRF
- Validation des entrées
- Hachage des mots de passe
- Sessions sécurisées

## 📧 Configuration Email

Pour activer les notifications par email, configurez les variables SMTP dans le fichier `.env`:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=votre_email@gmail.com
SMTP_PASSWORD=votre_mot_de_passe_application
```

## 🤖 Assistant Médical IA

L'assistant utilise l'API OpenRouter avec le modèle Llama 3.3 70B pour fournir:
- Informations médicales générales
- Recommandations de médicaments
- Conseils de santé
- Rappels de consulter un médecin

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Contribution

Les contributions sont les bienvenues! N'hésitez pas à:
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

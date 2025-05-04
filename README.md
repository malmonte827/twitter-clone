# 🐦 Twitter Clone

> A Flask-based microblogging app modeled after Twitter: signup/login, follow/unfollow, post messages, like/unlike, and edit your profile.

 [![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/) [![Flask](https://img.shields.io/badge/flask-2.2-brightgreen)](https://flask.palletsprojects.com/)

---

## 📋 Table of Contents

1. [About](#about)  
2. [Features](#features)  
3. [Tech Stack](#tech-stack)  
4. [Getting Started](#getting-started)  
   - [Prerequisites](#prerequisites)  
   - [Installation](#installation)  
   - [Database Setup & Seeding](#database-setup--seeding)  
5. [Usage](#usage)  
6. [Testing](#testing)  
7. [Contributing](#contributing)  
9. [Contact](#contact)  

---

## 🌟 About

This is a simple Twitter-style “Warbler” clone built with Flask. Users can:

- Sign up, log in/out  
- Follow and unfollow other users  
- Post short messages (“warbles”)  
- Like or unlike messages  
- Edit their profile (bio, images)  
- Browse the 100 most recent messages  

All data is stored in PostgreSQL, and the UI is rendered with Jinja2 templates.

---

## ✨ Features

- **User Auth**: Secure signup & login with hashed passwords  
- **Profiles**: View & edit your profile (username, bio, header & profile images)  
- **Social**: Follow/unfollow other users & see their posts  
- **Posting**: Create, view, and delete your messages  
- **Likes**: Like/unlike any message  
- **Feed**: Personalized home feed of the latest 100 messages  
- **Forms & Validation**: WTForms with CSRF protection  
- **Dev Tools**: Flask-DebugToolbar integration  

---

## 🛠 Tech Stack

- **Language & Framework:** Python, Flask  
- **Database & ORM:** PostgreSQL, SQLAlchemy  
- **Forms:** WTForms  
- **Templates:** Jinja2 (HTML/CSS)  
- **Debugging:** flask-debugtoolbar  
- **Testing:** pytest  
- **Other:** GitHub Actions for CI  

---

## 🏁 Getting Started

### Prerequisites

- Python 3.8 or higher  
- PostgreSQL installed & running  
- `virtualenv` (optional but recommended)  

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/malmonte827/twitter-clone.git
cd twitter-clone

# 2. Create & activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```
---

### Database Setup & Seeding

```bash
# 4. Create your local database
createdb warbler

# 5. Set environment variables
export DATABASE_URL=postgresql:///warbler
export SECRET_KEY='your-secret-key'

# 6. Run the seed script to populate tables
python seed.py
```
---
### 📖 Usage

```bash
# Start the Flask app
flask run
```
---
### 🧪 Testing
```bash
# Run all unit & view tests
pytest
```
## Contributing

We welcome contributions! To contribute:

- Fork the repository

- Create a new branch (git checkout -b feature-name)

- Commit your changes (git commit -m 'Add new feature')

- Push to the branch (git push origin feature-name)

- Open a pull request

## Contact

For questions or suggestions, reach out:

- Email: malmonte827@gmail.com


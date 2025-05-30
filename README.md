# Fastapi-MySql
# 📘 FastAPI Blog & CSV Uploader API

A FastAPI-based RESTful API that supports:

- CRUD operations on blog posts and users
- Uploading CSV files to MySQL
- Exporting CSV files from MySQL
- Basic HTTP authentication for sensitive endpoints

## 🚀 Features

- ✅ FastAPI backend with automatic Swagger docs
- ✅ SQLAlchemy ORM for MySQL database
- ✅ Basic Auth-protected CSV import/export
- ✅ Docker-compatible
- ✅ Pandas for CSV processing

---

## 🛠️ Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- MySQL (tested with 8.x)
- Pandas

---

🚀 Getting Started

1. Clone the Repository

    git clone https://github.com/sanasikandar/Fastapi-MySql.git
    cd fastapi-blog-csv-api

2. Create and Activate a Virtual Environment

    python -m venv venv

    # For Linux/macOS
    source venv/bin/activate

    # For Windows
    venv\Scripts\activate

3. Install Dependencies

    pip install -r requirements.txt

---

🛠️ MySQL Setup

Run the following SQL commands in your MySQL client or CLI:

    CREATE DATABASE tododb;
    CREATE USER 'devuser'@'%' IDENTIFIED BY 'devpass';
    GRANT ALL PRIVILEGES ON tododb.* TO 'devuser'@'%';
    FLUSH PRIVILEGES;

⚠️ Make sure the MySQL connection details in main.py match your local setup.

---

▶️ Run the App

    uvicorn main:app --reload

Open your browser and navigate to:
Swagger UI: http://localhost:8000/docs

---

📂 API Endpoints

🔐 Authentication

Basic HTTP Authentication is required for CSV upload/export.
Username: admin
Password: secret

---

📄 Blog Posts

- POST /posts/ – Create a post
- GET /posts/{id} – Get a post by ID
- DELETE /posts/{id} – Delete a post

---

👤 Users

- POST /users/ – Create a user
- GET /users/{id} – Get a user

---

📤 Upload CSV to MySQL

- Endpoint: POST /upload-csv
- Form Field: file (CSV file)
- Authentication Required

    curl -u admin:secret -F "file=@mount.csv" http://localhost:8000/upload-csv

---

📥 Export MySQL Table to CSV

- Endpoint: GET /export-csv
- Authentication Required

    curl -u admin:secret http://localhost:8000/export-csv -o mountaineers.csv

---

📁 Example CSV Format

    id,Name,Age,Expedition,Nationality,Height
    1,John Doe,32,Everest,USA,180.5
    2,Jane Smith,28,K2,UK,170.2

---

🧪 Testing

Use the Swagger UI to test all available endpoints:
http://localhost:8000/docs

---

📬 Contact

Created with  by Sana Sikandar
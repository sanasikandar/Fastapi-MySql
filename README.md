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

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/sanasikandar/Fastapi-BE
cd fastapi-blog-csv-api

2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate


3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Set Up MySQL Database
Create a MySQL database and user:

sql
Copy
Edit
CREATE DATABASE tododb;
CREATE USER 'devuser'@'%' IDENTIFIED BY 'devpass';
GRANT ALL PRIVILEGES ON tododb.* TO 'devuser'@'%';
FLUSH PRIVILEGES;
⚙️ Configuration
Update your MySQL connection details in main.py if needed:

python
Copy
Edit
host='localhost',
port=3306,
user='devuser',
password='devpass',
database='tododb'
▶️ Run the App
bash
Copy
Edit
uvicorn main:app --reload
Access docs at: http://localhost:8000/docs

📂 API Endpoints
🔐 Authentication
Basic HTTP Auth (username: admin, password: secret) is required for CSV operations.

📄 Blog Posts
POST /posts/ – Create a post

GET /posts/{id} – Get a post by ID

DELETE /posts/{id} – Delete a post

👤 Users
POST /users/ – Create a user

GET /users/{id} – Get a user

📤 Upload CSV to MySQL
Endpoint: POST /upload-csv

Form Field: file (CSV File)

Auth Required: ✅

bash
Copy
Edit
curl -u admin:secret -F "file=@mount.csv" http://localhost:8000/upload-csv
📥 Export MySQL Table to CSV
Endpoint: GET /export-csv

Auth Required: ✅

bash
Copy
Edit
curl -u admin:secret http://localhost:8000/export-csv -o mountaineers.csv
📁 Example CSV Format
csv
Copy
Edit
id,Name,Age,Expedition,Nationality,Height
1,John Doe,32,Everest,USA,180.5
2,Jane Smith,28,K2,UK,170.2
🧪 Testing
Use Swagger UI at http://localhost:8000/docs to interact with all endpoints easily.


from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import pandas as pd
import mysql.connector
import secrets
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session 
from fastapi.responses import FileResponse
from fastapi import UploadFile, File
import io # handle the in memory in csv 



app = FastAPI()
security = HTTPBasic()
models.Base.metadata.create_all(bind=engine)


class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    username: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get credentials
VALID_USERNAME = "admin"
VALID_PASSWORD = "secret"

db_dependency = Annotated[Session, Depends(get_db)]  


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()

@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def read_post(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail='Post not found')
    return post

@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db: db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Post was not found')
    db.delete(db_post)
    db.commit()


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)  
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user

    


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, VALID_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, VALID_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/export-csv", response_class=FileResponse)
def export_csv(user: str = Depends(authenticate)):
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='devuser',
            password='devpass',
            database='tododb'
        )

        # Query the table
        query = "SELECT * FROM mountaineers"
        df = pd.read_sql(query, conn)

        # Save to CSV
        csv_path = "/tmp/mountaineers_export.csv"
        df.to_csv(csv_path, index=False)

        # Return file for download
        return FileResponse(
            path=csv_path,
            filename="mountaineers.csv",
            media_type="text/csv"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn.is_connected():
            conn.close()


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...), user: str = Depends(authenticate)):
    try:
        # Read file contents
        contents = await file.read()

        # Load CSV data into DataFrame
        df = pd.read_csv(io.BytesIO(contents))

        # Connect to MySQL
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='devuser',
            password='devpass',
            database='tododb'
        )
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS mountaineers (
            id INT PRIMARY KEY,
            Name VARCHAR(100),
            Age INT,
            Expedition VARCHAR(100),
            Nationality VARCHAR(50),
            Height FLOAT
        )
        """)

        # Insert or update data
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO mountaineers (id, Name, Age, Expedition, Nationality, Height)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    Name=VALUES(Name),
                    Age=VALUES(Age),
                    Expedition=VALUES(Expedition),
                    Nationality=VALUES(Nationality),
                    Height=VALUES(Height)
            """, tuple(row))

        conn.commit()
        return {"message": "CSV uploaded and database updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload CSV: {str(e)}")
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()
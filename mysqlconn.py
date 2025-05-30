import pandas as pd
import mysql.connector

# Load the CSV file (host path mounted into the container)
df = pd.read_csv('/home/sana/mysql-files/mount.csv')

# Connect to MySQL (Docker container running locally)
conn = mysql.connector.connect(
    host='localhost',       
    port=3306,
    user='devuser',
    password='devpass',
    database='tododb'
)
cursor = conn.cursor()

# Create the table
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

# Insert data into the table
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

# Commit and close connection
conn.commit()
cursor.close()
conn.close()

from fastapi import FastAPI 
from pydantic import BaseModel 
from datetime import datetime
import mysql.connector
import base64

app = FastAPI()

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        port=3306,
        password="1234",
        database="test_1"
    )
    print("Connected to MySQL database")

except mysql.connector.Error as err:
    print(f"Error connecting to MySQL database: {err}")

cur = connection.cursor()

# Execute a query
cur.execute("SELECT * FROM posts")

# Fetch one result
row = cur.fetchall()
print(row)

# Close connection
#connection.close()

class Post(BaseModel):
    post_id:int
    title:str
    content:str
    image_url:str
    created_at:datetime
    likes:int

@app.get("/")
async def root():
    return {"message":"is this working"}

@app.get("/posts")
async def get_posts(post:Post):
    #encoded_post = base64.b64encode(post.json())
    return post
    
from fastapi import FastAPI 
from pydantic import BaseModel 
from datetime import datetime
import mysql.connector
import base64

app = FastAPI()




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
async def get_posts():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        port=3306,
        password="1234",
        database="sys"
        )
    print("Connected to MySQL database")

    cur = connection.cursor()
    posts=cur.execute("SELECT * FROM posts")
    posts=cur.fetchall()
    encoded_posts=[]
    for post in posts:
        encoded_posts.append(await convert_base64(post))
    return {"posts":encoded_posts}

#could we use caching to make it fast? SQLAlchemy


async def convert_base64(post:Post):
    encoded_post=await(base64.b64encode(post.encode('utf-8')))
    return encoded_post
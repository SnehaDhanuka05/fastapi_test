from fastapi import FastAPI 
from pydantic import BaseModel 
from datetime import datetime
import mysql.connector
import base64
from functools import cache
import time
from pathlib import Path

app = FastAPI()

# Close connection
#connection.close()
#do we use this block?

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


image_dir = Path("/Users/sneha/fastapi/images")

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
    #removed try and except, connection was showing as undefined variable
    cur = connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS posts (post_id INT PRIMARY KEY, title VARCHAR(255), content TEXT, image_url VARCHAR(255), created_at DATETIME, likes INT)")
    cur.execute("INSERT INTO posts(post_id, title, content, image_url, created_at, likes) VALUES (1, 'best food in town', 'awesome restaurants to try!', '/Users/sneha/fastapi/images.jpeg', NOW(), 5)")
    posts=cur.execute("SELECT * FROM posts")
    posts=cur.fetchall()

#used AI to get this block of code to bulk insert urls in the table
    for i, image_path in enumerate(image_dir.iterdir(), start=2):
        if image_path.is_file():
            cur.execute(
            """
            INSERT INTO posts (post_id, title, content, image_url, created_at, likes)
            VALUES (%s, %s, %s, %s, NOW(), %s)
            """,
            (
                i,
                f"Image {i}",
                "Image from folder",
                str(image_path),   # or image_path.name
                0
            )
        )

    image_urls=[]
    image_urls=cur.execute("SELECT image_url FROM posts")
    image_urls=cur.fetchall()
    print(image_urls)

    start_time = time.time()
    encoded_posts=[]
    for urls in image_dir.iterdir():
        print(urls)
        encoded_posts.append(await convert_base64(urls))
    end_time = time.time()

    print(f"Time taken: {end_time - start_time}")

    return {"posts": encoded_posts}

#could we use caching to make it fast? SQLAlchemy?
#for stale cache, we can use TTL ofc but also learnt about Debezium. uses kafka to stream chnages from logs of db
#for mysql, aiomysql can be used

#@cache
async def convert_base64(image_url: str):
    print(image_url)
    with open(image_url, "rb") as img:
        s=base64.b64encode(img.read()).decode("utf-8")
    return s 
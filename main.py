from fastapi import FastAPI 
from pydantic import BaseModel 
from datetime import datetime
import mysql.connector
import base64
from functools import cache
import time
import asyncio
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from async_hybrid_cache import CacheOptions, AsyncHybridCache

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

#cache
cache = AsyncHybridCache(
        options=CacheOptions(
            ttl=60,
            fail_safe_seconds=300,
            lru_max_keys=50,
        ),
    )

@app.get("/")
async def root():
    return {"message":"is this working"}


def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        port=3306,
        password="1234",
        database="fastapi_task"
        )
    print("Connected to MySQL database")
    #removed try and except, connection was showing as undefined variable
    cur = connection.cursor()
    #cur.execute("CREATE TABLE IF NOT EXISTS posts (post_id INT PRIMARY KEY, title VARCHAR(255), content TEXT, image_url VARCHAR(255), created_at DATETIME, likes INT)")
    #cur.execute("INSERT INTO posts(post_id, title, content, image_url, created_at, likes) VALUES (1, 'best food in town', 'awesome restaurants to try!', '/Users/sneha/fastapi/images.jpeg', NOW(), 5)")
    #posts=cur.execute("SELECT * FROM posts")
    #posts=cur.fetchall()

    
    image_urls=cur.execute("SELECT image_url FROM new_post")
    image_urls=cur.fetchall()
    return image_urls

#image_dir = Path("/Users/sneha/fastapi/images")

def get_image_urls():
    image_urls = get_db_connection()
    return image_urls

@app.get("/posts")
async def get_posts():
    
    start_time = time.time()
    encoded_posts=[]
    # for urls in image_urls:
    #     encoded_posts.append(await asyncio.gather(convert_base64(urls[0])))
    tasks=[]
    image_urls = get_image_urls()
    async with asyncio.TaskGroup() as tg:
        for urls in image_urls:
            if os.path.exists(urls[0]):
                task=tg.create_task(convert_base64(urls[0]))
                tasks.append(task)
            else:
                print(f"image dont exist: {urls[0]}")    

    encoded_posts=[task.result() for task in tasks]
    end_time = time.time()

    print(f"Time taken: {end_time - start_time}")

    return {"posts": encoded_posts}

#could we use caching to make it fast? SQLAlchemy?
#for stale cache, we can use TTL ofc but also learnt about Debezium. uses kafka to stream chnages from logs of db
#for mysql, aiomysql can be used


#@cache
async def convert_base64(image_url: str):
    with open(image_url, "rb") as img:
        s=base64.b64encode(img.read()).decode("utf-8")
    return s

async def fetch_image_from_db(url:str):
    image_urls = get_image_urls()
    return image_urls.get(url)

@cache.cached(
    lambda url: url,
    options=CacheOptions(ttl_seconds=60, lru_max_keys=50)
)

async def load_image(url:str):
    image_data=await fetch_image_from_db(url)
    return image_data

async def get_image(url:str):
    return await load_image(url)
    

async def update_image(url:str):
    if load_image.cache.has(url):
        url.mtime!=load_image.cache.get(url).mtime
        load_image.cache.delete(url)


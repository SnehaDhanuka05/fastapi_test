from fastapi import FastAPI
import pymongo
import asyncio
import mysql.connector
import time

app = FastAPI()

cache =[]

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["test_posts"]
collection = db["task1"]

connection = mysql.connector.connect(
        host="localhost",
        user="root",
        port=3306,
        password="1234",
        database="fastapi_task"
        )
print("Connected to MySQL database")

 

@app.get("/shippingDetails/{orderId}")
async def get_shippingDetails(orderId: str):
    cur = connection.cursor()
    cur.execute("SELECT * FROM shipping_details WHERE orderId = %s ",(orderId,))
    shipping_fetched = cur.fetchone()
    shipping_details = {
        "address": {
            "street": shipping_fetched[1],
            "city": shipping_fetched[2],
            "state": shipping_fetched[3],
            "postalCode": shipping_fetched[4],
            "country": shipping_fetched[5],
            "coordinates": {"lat, lng": shipping_fetched[6]},
        },
        "method": {
            "carrier": shipping_fetched[7],
            "serviceLevel": shipping_fetched[8],
            "trackingHistory": [
            {
                "status": shipping_fetched[9],
                "location": shipping_fetched[10],
                "timestamp": shipping_fetched[11],
            }
        ],
       }
    }
    return shipping_details

@app.get("/get_orders")
async def get_all_orders():
    orders=collection.find({})
    order_list=[]
    for order in orders:
        order['_id'] = str(order['_id'])  # Convert ObjectId to string
        if get_order_from_cache(order.get("orderId")):
            if get_cached_order_updated_time(order.get("orderId")) > get_actual_updated_time(order.get("orderId")):
                get_order_from_cache(order.get("orderId"))
                order_list.append(order)
        else:
            orderId = order.get("orderId")
            shippingDetails = await get_shippingDetails(orderId)
            order["shippingDetails"] = shippingDetails
            order_list.append(order)
            cache_order(order)
        
    return order_list

def cache_order(order):
    cache.append(order)

def get_order_from_cache(orderId: str):
    for order in cache:
        if order["orderId"] == orderId:
            return order
    return None

def refresh_cache_updated_order_time(orderId: str):
    updated_time = get_actual_updated_time(orderId)
    for order in cache:
        if order["orderId"] == orderId:
            order["updated_time"] = updated_time[0]
            return
    cache.append({"orderId": orderId, "updated_time": updated_time[0]})

def get_cached_order_updated_time(orderId: str):
    for order in cache:
        if order["orderId"] == orderId:
            return str(order.get("updated_time"))
    return None

def get_actual_updated_time(orderId: str):
    cur=connection.cursor()
    cur.execute("SELECT updated_time FROM order_updates WHERE orderId = %s", (orderId,))
    updated_time = cur.fetchone()
    return updated_time[0]
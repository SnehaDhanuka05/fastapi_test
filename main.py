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
    cur.execute("SELECT * FROM address WHERE orderId = %s ",(orderId,))
    address_fetched = cur.fetchone()
    address = {
        "street": address_fetched[1],
        "city": address_fetched[2],
        "state": address_fetched[3],
        "postalCode": address_fetched[4],
        "country": address_fetched[5],
        "coordinates": {"lat, lng": address_fetched[6]},
    } 

    cur.execute("SELECT * FROM method WHERE orderId = %s" ,(orderId,))
    method_fetched = cur.fetchone()
    method = {
        "carrier": method_fetched[1],
        "serviceLevel": method_fetched[2],
        "trackingHistory": [
            {
                "status": method_fetched[3],
                "location": method_fetched[4],
                "timestamp": method_fetched[5],
            }
        ],
    }
    shippingDetails = {
        "address": address,
        "method": method
    }
    return shippingDetails

@app.get("/orders")
async def get_all_orders():
    orders=collection.find({})
    order_list=[]
    for order in orders:
        order['_id'] = str(order['_id'])  # Convert ObjectId to string
        if get_order_from_cache(order.get("orderId")):
            if get_cached_order_updated_time(order.get("orderId")) > get_actual_updated_time(order.get("orderId")):
                order_list.append(order)
        else:
            orderId = order.get("orderId")
            shippingDetails = await get_shippingDetails(orderId)
            order["shippingDetails"] = shippingDetails
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
            return order.get("updated_time")
    return None

def get_actual_updated_time(orderId: str):
    cur=connection.cursor()
    cur.execute("SELECT updated_time FROM orders WHERE orderId = %s", (orderId,))
    updated_time = cur.fetchone()
    if updated_time:
        return updated_time[0]
    return None
    

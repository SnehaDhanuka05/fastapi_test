from fastapi import FastAPI
import pymongo
import asyncio
import mysql.connector

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
    cache_shipping_details(orderId,shippingDetails)
    return shippingDetails

@app.get("/orders")
async def get_all_orders():
    orders=collection.find({})
    order_list=[]
    for order in orders:
        order['_id'] = str(order['_id'])  # Convert ObjectId to string
        order_list.append(order)
        orderId = order.get("orderId")
        if cache_shipping_details:
            order["shippingDetails"] = await get_cached_shipping_details(orderId)

        else:
            shippingDetails = await get_shippingDetails(orderId)
            order["shippingDetails"] = shippingDetails
            cache_shipping_details(orderId, shippingDetails)

    return order_list

def get_cached_shipping_details(orderId: str):
    for order in cache:
        if order["orderId"] == orderId:
            return order["shippingDetails"]
    return None

def cache_shipping_details(orderId: str, shippingDetails: dict):
    cache.append({"orderId": orderId, "shippingDetails": shippingDetails})


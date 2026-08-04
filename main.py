from bson import ObjectId
from fastapi import FastAPI
import pymongo
import asyncio
import mysql.connector

app = FastAPI()

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
cur = connection.cursor()
 

@app.get("/shippingDetails/{orderId}")
def get_shippingDetails(orderId: str):
    cur.execute("SELECT * FROM address WHERE orderId = %s ",(orderId,))
    address = cur.fetchone()
    cur.execute("SELECT * FROM method WHERE orderId = %s" ,(orderId,))
    method = cur.fetchone()
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
        order_list.append(order)

    for order in order_list:
        orderId = order.get("orderId")
        if orderId:
            shippingDetails = get_shippingDetails(orderId)
            order["shippingDetails"] = shippingDetails   
             
    return order_list



# def get_dfs(document, path=None):
#     if path is None:
#         path=[]
#     #results =[]
#     #if the node is a dict
#     if isinstance(document, dict):
#         for key, value in document.items():
#             if key == "_id" and isinstance(value, ObjectId):
#                 #results.append({"path": path + [key], "value": str(value)})
#                 yield {"path": path + [key], "value": str(value)}
#                 #yield str(value)
#             else:
#                 #results.extend(get_dfs(value, path + [key]))
#                 path.append(key)
#                 yield from get_dfs(value, path)
#                 path.pop()
#     #if the node is a list 

#     elif isinstance(document, list):
#         for index, item in enumerate(document):
#             #results.extend(get_dfs(item, path + [index]))
#             yield from get_dfs(item, path )
#     #the node is a string/integer value
#     else:
#         #results.append({"path": path, "value": document})
#         yield {"path": path, "value ": document}
#         #yield document

    #return results

     
# @app.post("/insert")
# def insert_document():
#     insert_this = {
#         "orderId": "ORD-987654321",
#         "customerId": "CUST-102938",
#         "orderStatus": "PROCESSING",
#         "timestamps": {
#             "created": "2024-10-27T10:00:00Z",
#             "updated": "2024-10-27T10:15:00Z",
#             "estimatedDelivery": "2024-11-05T00:00:00Z",
#         },
#         "shippingDetails": {
#             "address": {
#                 "street": "123 Main St",
#                 "city": "Anytown",
#                 "state": "CA",
#                 "postalCode": "90210",
#                 "country": "USA",
#                 "coordinates": {"lat": 34.0522, "lng": -118.2437},
#             },
#             "method": {
#                 "carrier": "FedEx",
#                 "serviceLevel": "Overnight",
#                 "trackingHistory": [
#                     {
#                         "status": "Label Created",
#                         "location": "Warehouse A",
#                         "timestamp": "2024-10-27T10:30:00Z",
#                     }
#                 ],
#             },
#         },
#         "payment": {
#             "method": "CREDIT_CARD",
#             "transactionId": "TXN-555444333",
#             "billingAddress": {"isSameAsShipping": True},
#             "breakdown": {
#                 "subtotal": 1250.00,
#                 "tax": 100.00,
#                 "shippingCost": 25.00,
#                 "discountsApplied": [
#                     {"code": "FALL20", "amount": 50.00, "type": "PERCENTAGE"}
#                 ],
#                 "total": 1325.00,
#             },
#         },
#         "items": [
#             {
#                 "productId": "PROD-A1",
#                 "sku": "SKU-A1-BLK-M",
#                 "quantity": 2,
#                 "unitPrice": 500.00,
#                 "productDetails": {
#                     "name": "High-End Laptop",
#                     "category": ["Electronics", "Computers", "Laptops"],
#                     "attributes": {
#                         "color": "Black",
#                         "size": "Medium",
#                         "weight": "1.5kg",
#                         "dimensions": {"length": 30, "width": 20, "height": 2},
#                     },
#                     "warranty": {
#                         "provider": "TechCare",
#                         "durationMonths": 24,
#                         "terms": "Standard limited warranty",
#                     },
#                 },
#                 "customizationOptions": [
#                     {"type": "Engraving", "value": "Happy Birthday", "cost": 25.00}
#                 ],
#             }
#         ],
#         "auditLog": [
#             {
#                 "action": "ORDER_CREATED",
#                 "user": "system",
#                 "timestamp": "2024-10-27T10:00:00Z",
#             }
#         ],
#         "metadata": {
#             "sourcePlatform": "Web",
#             "campaignId": "CAMP-HOLIDAY24",
#             "abTestGroup": "Variant-B",
#         },
#     }
#     result = collection.insert_one(insert_this)
#     return {"inserted_id": str(result.inserted_id)}
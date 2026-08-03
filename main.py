from fastapi import FastAPI
import pymongo

app = FastAPI()

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["test_posts"]
collection = db["task1"]
document = collection.find_one()
print("total content of tree", document)


# @app.get("/total_content")
# def fetch_documents():
#     docs = list(collection.find())
#     if not docs:
#         return {"message": "No documents found in the collection."}
#     else:
#         for doc in docs.children:
#             return fetch_documents(doc)

@app.get("/dfs")
def get_dfs(document, path="root"):
    #if the node is a dict
    if isinstance(document, dict):
        for key, value in document.items():
            get_dfs(value, {key})
    #if the node is a list 
    elif isinstance(document, list):
        for index, item in enumerate(document):
            get_dfs(item, [{index}])
    #the node is a primitive value
    else:
        return (f"{document}")

get_dfs(document)

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


    


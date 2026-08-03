import pymongo 


if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["test_posts"]
    collection = db["posts"]
    # first_post = collection.find_one({'post_id': 2})
    # print(first_post)
    # result=db.getCollection("posts")
    # print(result)
    collection_list = collection.find()
    for c in collection_list:
        print(c)
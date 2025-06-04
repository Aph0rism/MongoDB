from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

MONGO_URI = "mongodb://testuser:testpass@localhost:27017/testdb?authSource=testdb"

def connect(uri):
    try:
        client = MongoClient(uri)
        client.admin.command('ping')
        print("Connexion réussie à MongoDB")
        return client
    except ConnectionFailure:
        print("Erreur de connexion")
        return None

def insert_document(db):
    result = db.testcoll.insert_one({'name': 'Charlie', 'age': 28})
    print("ID inséré:", result.inserted_id)

def query_documents(db):
    for doc in db.testcoll.find({'age': {'$gt': 20}}):
        print(doc)

def update_document(db):
    db.testcoll.update_one({'name': 'Charlie'}, {'$set': {'age': 29}})

def delete_document(db):
    db.testcoll.delete_one({'name': 'Charlie'})

if __name__ == "__main__":
    client = connect(MONGO_URI)
    db = client['testdb']
    insert_document(db)
    query_documents(db)
    update_document(db)
    query_documents(db)
    delete_document(db)
    query_documents(db)
from pymongo import MongoClient

def test_insert_and_find():
    client = MongoClient("mongodb://testuser:testpass@localhost:27017/testdb?authSource=testdb")
    db = client['testdb']
    doc_id = db.testcoll.insert_one({'name': 'Test', 'age': 99}).inserted_id
    doc = db.testcoll.find_one({'_id': doc_id})
    assert doc['name'] == 'Test'
    db.testcoll.delete_one({'_id': doc_id})
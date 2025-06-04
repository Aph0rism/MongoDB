db = db.getSiblingDB('testdb');
db.createUser({
  user: 'testuser',
  pwd: 'testpass',
  roles: [{role: 'readWrite', db: 'testdb'}]
});
db.testcoll.insertMany([
  {name: 'Alice', age: 25},
  {name: 'Bob', age: 30}
]);
db.createUser({
  user: "student",
  pwd: "student123",
  roles: [{ role: "readWrite", db: "pythonde" }]
});

db = db.getSiblingDB("pythonde");

db.users.insertMany([
  {
    username: "alice",
    email: "alice@example.com",
    profile: { age: 25, city: "Berlin" },
    created_at: new Date()
  },
  {
    username: "bob",
    email: "bob@example.com",
    profile: { age: 30, city: "Munich" },
    created_at: new Date()
  }
]);

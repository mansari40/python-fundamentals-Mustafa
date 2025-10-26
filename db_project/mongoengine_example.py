from mongoengine import (
    Document,
    StringField,
    IntField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    DateTimeField,
    connect,
    ListField,
    EmbeddedDocumentListField,
)
from datetime import datetime
from pymongo_example import MongoUser, MongoUserList

MONGO_URL = "mongodb://root:secret@localhost:27017/"
connect("pythonde", host=MONGO_URL)


class Purchase(EmbeddedDocument):  
    purchase_id = IntField(required=True)
    product = StringField(required=True)
    amount = IntField(min_value=0)


class Profile(EmbeddedDocument):
    age = IntField(min_value=0, max_value=120)
    city = StringField(max_length=100)
    hobbies = ListField(StringField()) 


class User(Document):
    meta = {"collection": "users", "indexes": ["username", "email"]}

    username = StringField(required=True, unique=True, max_length=50)
    email = StringField(required=True)
    profile = EmbeddedDocumentField(Profile)
    created_at = DateTimeField(default=datetime.utcnow)
    purchases = EmbeddedDocumentListField(Purchase) 


def list_users() -> list[MongoUser]:
    users = User.objects.all().as_pymongo() 
    return MongoUserList.validate_python(list(users))


def create_user(username: str, email: str, age: int, city: str) -> None:
    profile = Profile(age=age, city=city, hobbies=["music", "sports"])
    user = User(username=username, email=email, profile=profile)
    user.save()
    print(f"User '{username}' added to MongoDB via MongoEngine.")


def update_user_city(username: str, new_city: str) -> None:
    user = User.objects(username=username).first()
    if not user:
        print(f"No user found with name '{username}'.")
        return
    user.profile.city = new_city
    user.save()
    print(f"Updated '{username}' city to '{new_city}'.")


if __name__ == "__main__":
    User.objects.delete()  

    create_user("alice", "alice@example.com", 27, "Berlin")
    create_user("ahmad", "ahmad@example.com", 34, "Munich")

    print("\nAll users in MongoDB:")
    for user in list_users():
        print(
            f"Username: {user.username}, Email: {user.email}, Created At: {user.created_at}"
        )

    print("\nUpdate user city:")
    update_user_city("ahmad", "Hamburg")

    users = list_users()
    with open("data/mongoengine_users.json", "wb") as f:
        f.write(MongoUserList.dump_json(users, indent=2))

    print("\nUpdated data exported to data/mongoengine_users.json")

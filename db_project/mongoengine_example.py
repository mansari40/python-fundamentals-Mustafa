from mongoengine import (
    Document,
    StringField,
    IntField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    DateTimeField,
    ListField,
    connect,
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

    username = StringField(required=True, unique=True)
    email = StringField(required=True)
    profile = EmbeddedDocumentField(Profile)
    created_at = DateTimeField(default=datetime.utcnow)
    purchases = ListField(EmbeddedDocumentField(Purchase))


def list_users() -> list[MongoUser]:
    users = User.objects.all().as_pymongo() 
    return MongoUserList.validate_python(list(users))

def create_user(username: str, email: str, age: int, city: str) -> None:
    profile = Profile(age=age, city=city, hobbies=["music", "sports"])
    user = User(username=username, email=email, profile=profile)
    user.save()


def update_user_city(username: str, new_city: str) -> None:
    user = User.objects(username=username).first()
    if user:
        user.profile.city = new_city
        user.save()


if __name__ == "__main__":
    print("All users in MongoDB:")
    for user in list_users():
        print(
            [user.id],
            f"Username: {user.username}, Email: {user.email}, Created At: {user.created_at}",
        )

    users = list_users()

    with open("data/mongoengine_users.json", "wb") as f:
        f.write(MongoUserList.dump_json(users, indent=2))

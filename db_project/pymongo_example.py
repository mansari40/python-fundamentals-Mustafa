from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel, Field, TypeAdapter, field_validator
from pymongo import MongoClient

MONGO_URL = "mongodb://root:secret@localhost:27017/"
client: MongoClient[dict[str, Any]] = MongoClient(MONGO_URL)
users_col = client.pythonde.users


class Profile(BaseModel):
    class Config:
        from_attributes = True

    age: int | None = None
    city: str | None = None
    interests: list[str] | None = None


class MongoUser(BaseModel):
    class Config:
        from_attributes = True

    id: str = Field(alias="_id")
    username: str
    email: str
    profile: Profile
    created_at: datetime | None = None

    @field_validator("id", mode="before")
    @classmethod
    def validate_object_id(cls, v: Any) -> str:
        return str(v)


MongoUserList = TypeAdapter(list[MongoUser])


def create_user(username: str, email: str, age: int, city: str) -> None:
    user = {
        "username": username,
        "email": email,
        "profile": {"age": age, "city": city, "interests": ["music", "travel"]},
        "created_at": datetime.now(timezone.utc),
    }
    users_col.insert_one(user)
    print(f"User '{username}' created.")


def list_users() -> list[MongoUser]:
    users = users_col.find()
    cleaned = []
    for user in users:
        user["_id"] = str(user["_id"])  
        cleaned.append(user)
    return MongoUserList.validate_python(cleaned)


def get_user_by_username(username: str) -> MongoUser | None:
    user_data = users_col.find_one({"username": username})
    if user_data:
        user_data["_id"] = str(user_data["_id"])
        return MongoUser.model_validate(user_data)
    return None


def update_user_city(username: str, new_city: str) -> None:
    result = users_col.update_one(
        {"username": username},
        {"$set": {"profile.city": new_city}},
    )
    if result.modified_count:
        print(f"Updated '{username}' city to '{new_city}'.")
    else:
        print(f"No update for '{username}'.")


if __name__ == "__main__":
    users_col.delete_many({})  

    create_user("alice", "alice@example.com", 27, "Berlin")
    create_user("ahmad", "ahmad@example.com", 34, "Bremen")

    print("\nAll users:")
    for user in list_users():
        print(user)

    print("\nFind user (alice):")
    print(get_user_by_username("alice"))

    print("\nUpdate user city:")
    update_user_city("ahmad", "Hamburg")

    print("\nAll users after update:")
    for user in list_users():
        print(user)

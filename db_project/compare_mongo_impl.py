from pymongo_example import (
    create_user as create_user_pymongo,
    list_users as list_users_pymongo,
    update_user_city as update_city_pymongo,
)
from mongoengine_example import (
    create_user as create_user_me,
    list_users as list_users_me,
    update_user_city as update_city_me,
    User,
)
from mongoengine import connect
from pprint import pprint

connect("pythonde", host="mongodb://root:secret@localhost:27017/")
User.objects.delete()


create_user_pymongo("john", "john@example.com", 29, "Berlin")
create_user_pymongo("sara", "sara@example.com", 31, "Munich")
update_city_pymongo("john", "Hamburg")

print("\nPyMongo users:")
pymongo_users = [u.model_dump() for u in list_users_pymongo()]
pprint(pymongo_users)

User.objects.delete()

try:
    create_user_me("john", "john@example.com", 29, "Berlin")
    create_user_me("sara", "sara@example.com", 31, "Munich")
    update_city_me("john", "Hamburg")
except Exception as e:
    print(f"Error during MongoEngine test: {e}")

print("\nMongoEngine users:")
mongoengine_users = [u.model_dump() for u in list_users_me()]
pprint(mongoengine_users)

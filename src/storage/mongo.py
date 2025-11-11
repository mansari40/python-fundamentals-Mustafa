from mongoengine import connect

MONGO_URL = "mongodb://root:secret@localhost:27017/"
DB_NAME = "pythonde"

connect(DB_NAME, host=MONGO_URL)

from pymongo import MongoClient
from pymongo.errors import PyMongoError

client = None
db = None

def init_db(app):
    global client, db
    mongo_uri = app.config.get('MONGO_URI')
    db_name = app.config.get('MONGO_DB_NAME', 'skyforge')

    if not mongo_uri:
        raise RuntimeError('MONGO_URI is not configured')

    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    try:
        client.admin.command('ping')
    except PyMongoError as exc:
        raise RuntimeError(f'Unable to connect to MongoDB at {mongo_uri}: {exc}') from exc

    db = client[db_name]
    db.users.create_index('email', unique=True)
    db.users.create_index('phone', unique=True)

def get_db():
    return db

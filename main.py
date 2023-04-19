import os
from dotenv import load_dotenv
import pymongo
load_dotenv()

MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")

client = MONGO_CONNECTION_STRING
db = client['test']
col = db['playlistitemsschemas']

rec = col.find({}, {'_id': 0})
for i in rec:
    print(i)


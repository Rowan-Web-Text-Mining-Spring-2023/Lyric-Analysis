import pymongo

client = pymongo.MongoClient('mongodb+srv://Admin:TQ81m9PbqJvEKNOv@cluster0.ca1yfqc.mongodb.net/test')
db = client['test']
col = db['playlistitemsschemas']

rec = col.find({}, {'_id': 0})
for i in rec:
    print(i)


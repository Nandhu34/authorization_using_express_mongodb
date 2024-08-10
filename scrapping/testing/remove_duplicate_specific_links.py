import pymongo 
from bson import ObjectId

conn = pymongo.MongoClient('mongodb://localhost:27017')

db = conn['nandhaNaturals']

coll = db['duplicate_specific_product_links']

aggregate_query = [
    {
        '$group': {
            '_id': '$specific_prodict_links', 
            'sum': {
                '$sum': 1
            }, 
            'obj_id': {
                '$push': '$_id'
            }
        }
    }, {
        '$sort': {
            'sum': -1
        }
    }, {
        '$match': {
            'sum': {
                '$gt': 1
            }
        }
    }
]
data = list(coll.aggregate(aggregate_query))

# print(data)
for i in data:
    obj_id= i['obj_id']
    print(obj_id)
    obj_id.pop()
    for j in obj_id:
        print(j)
        delete = coll.delete_one({"_id":ObjectId(j)})
        print(delete.deleted_count)
        print(" deleted id ",j)

    
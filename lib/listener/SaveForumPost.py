import pymongo
import arrow
import falcon

from lib.config import Config

class SaveForumPost:
  def on_post(self, req, res):
    doc          = req.context["doc"]
    post         = doc["post"]
    crawler_name = doc["crawlerName"]
    country      = doc["country"]
    client       = pymongo.MongoClient("mongodb://{}/ardegra".format(Config.DATABASE_ADDRESS))
    try:
      entry_date = post["entryDate"]
      entry_date = arrow.get(entry_date).to("utc").isoformat()
      
      post.update({"_insert_time": arrow.utcnow().datetime})
      post.update({"category": "Forum"})
      post.update({"crawlerName": crawler_name})
      post.update({"country": country})
      post.update({"entryDate": entry_date})
      
      db                    = client["ardegra"]
      inserted_id           = db["mention"].insert_one(post).inserted_id
      res.context["result"] = {"insertedId": str(inserted_id), "duplicate": False}
      res.status            = falcon.HTTP_200
    except pymongo.errors.DuplicateKeyError:
      res.context["result"] = {"insertedId": None, "duplicate": True}
      res.status            = falcon.HTTP_200
    finally:
      client.close()
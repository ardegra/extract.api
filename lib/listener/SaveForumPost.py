import sys

import pymongo
import arrow
import falcon

from raven import Client
from logbook import Logger, StreamHandler
from lib.config import Config

class SaveForumPost:
  def on_post(self, req, res):
    doc          = req.context["doc"]
    post         = doc["post"]
    crawler_name = doc["crawlerName"]
    country      = doc["country"]
    client       = pymongo.MongoClient("mongodb://{}/ardegra".format(Config.DATABASE_ADDRESS))
    raven_client = Client()
    
    StreamHandler(sys.stdout).push_application()
    logger = Logger("SaveForumPost")
    
    try:
      logger.debug("Attemping to save: {}".format(post["permalink"]))
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
      
      logger.debug("Saved: {}".format(post["permalink"]))
    except pymongo.errors.DuplicateKeyError:
      logger.debug("Duplicate document: {}".format(post["permalink"]))
      res.context["result"] = {"insertedId": None, "duplicate": True}
      res.status            = falcon.HTTP_200
    finally:
      client.close()
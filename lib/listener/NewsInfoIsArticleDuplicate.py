import sys

import pymongo
import falcon

from lib.config import Config

from raven import Client
from logbook import Logger, StreamHandler

class NewsInfoIsArticleDuplicate:
  def on_post(self, req, res):
    doc = req.context["doc"]
    url = doc["url"]
    
    raven_client = Client()
    StreamHandler(sys.stdout).push_application()
    logger = Logger("NewsInfoIsArticleDuplicate")
    
    client = pymongo.MongoClient("mongodb://{}/ardegra".format(Config.DATABASE_ADDRESS))
    try:
      logger.debug("checking url: {}".format(url))
      db        = client["ardegra"]
      document  = db.mention.find_one({"permalink": url})
      duplicate = True if document is not None else False
      
      res.context["result"] = {"duplicate": duplicate, "error": {"message": "success", "code": 200}}
      res.status            = falcon.HTTP_200
    except Exception as err:
      raven_client.captureException()
      logger.error(str(err))
      res.context["result"] = {"error": {"message": str(err), "code": 404}}
      res.status            = falcon.HTTP_404
    finally:
      client.close()
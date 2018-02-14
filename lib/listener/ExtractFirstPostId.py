import sys

import weblib
import falcon
import pymongo

from lib.config import Config

from raven import Client
from logbook import Logger, StreamHandler
from grab import Grab

class ExtractFirstPostId:
  def on_post(self, req, res):
    doc          = req.context["doc"]
    url          = doc["url"]
    xpath        = doc["xpath"]
    
    raven_client = Client()
    StreamHandler(sys.stdout).push_application()
    logger = Logger("ExtractFirstPostId")
    
    client = pymongo.MongoClient("mongodb://{}/ardegra".format(Config.DATABASE_ADDRESS))
    try:
      logger.debug("url: {}".format(url))
      grab   = Grab()
      page   = grab.go(url)
      
      first_post_id_item = page.select(xpath["post"]["firstPostId"])
      first_post_id      = first_post_id_item.text()
      
      db        = client["ardegra"]
      document  = db["mention"].find_one({"id": first_post_id})
      duplicate = False if document is None else True
    except Exception as err:
      raven_client.captureException()
      logger.error(str(err))
      first_post_id = None
      duplicate     = None
    finally:
      client.close()

    logger.debug("firstPostId: {} | duplicate: {}".format(first_post_id, duplicate))
    res.context["result"] = {"firstPostId": first_post_id, "duplicate": duplicate}
    res.status            = falcon.HTTP_200
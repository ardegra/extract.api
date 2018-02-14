import sys

import pymongo
import falcon
import arrow
import requests

from raven import Client
from logbook import Logger, StreamHandler
from falcon.testing import simulate_post

from lib.parser.ParseEntryDate import ParseEntryDate as PED
from lib.config import Config

class SaveNewsArticle:
  def on_post(self, req, res):
    doc               = req.context["doc"]
    article           = doc["article"]
    country           = doc["country"]
    crawler_name      = doc["crawlerName"]
    entry_date_parser = doc["entryDateParser"]
    permalink         = doc["permalink"]
    raven_client      = Client()
    
    StreamHandler(sys.stdout).push_application()
    logger = Logger("SaveNewsArticle")
    
    client = pymongo.MongoClient("mongodb://{}/ardegra".format(Config.DATABASE_ADDRESS))
    try:
      article.update({"crawlerName": crawler_name})
      article.update({"country": country})
      article.update({"category": "News"})
      article.update({"_insert_time": arrow.utcnow().datetime})
      article.update({"permalink": permalink})
      logger.debug("Attempting to save: {}".format(article["permalink"]))
      
      logger.debug("Getting entry date with parser: {}".format(entry_date_parser))
      entry_date = PED.parse(entry_date_parser, article["entryDate"])
      entry_date = arrow.get(entry_date).datetime
      logger.debug("Here we go: {}".format(entry_date.isoformat()))
      article.update({"entryDate": entry_date})

      db          = client["ardegra"]
      inserted_id = db.mention.insert_one(article).inserted_id
      
      res.context["result"] = {"insertedId": str(inserted_id), "duplicate": False}
      res.status            = falcon.HTTP_200
      logger.debug("Saved: {}".format(permalink))
    except pymongo.errors.DuplicateKeyError as err:
      logger.debug("Duplicate document: {}".format(permalink))
      res.context["result"] = {"insertedId": None, "duplicate": True}
      res.status            = falcon.HTTP_200
    except Exception as ex:
      raven_client.captureException()
      logger.error(str(ex))
    finally:
      client.close()
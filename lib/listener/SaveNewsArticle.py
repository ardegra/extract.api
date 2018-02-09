import pymongo
import falcon
import arrow
import requests

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
    
    client = pymongo.MongoClient("mongodb://{}/ardegra".format(Config.DATABASE_ADDRESS))
    try:
      article.update({"crawlerName": crawler_name})
      article.update({"country": country})
      article.update({"category": "News"})
      article.update({"_insert_time": arrow.utcnow().datetime})
      article.update({"permalink": permalink})
      
      print("[SaveNewsArticle] Getting entry date with parser: {}".format(entry_date_parser))
      entry_date = PED.parse(entry_date_parser, article["entryDate"])
      entry_date = arrow.get(entry_date).datetime
      print("[SaveNewsArticle] Here we go: {}".format(entry_date.isoformat()))
      article.update({"entryDate": entry_date})

      db          = client["ardegra"]
      inserted_id = db.mention.insert_one(article).inserted_id
      
      res.context["result"] = {"insertedId": str(inserted_id), "duplicate": False}
      res.status            = falcon.HTTP_200
    except pymongo.errors.DuplicateKeyError as err:
      print("[SaveNewsArticle] Error: {}".format(str(err)))
      res.context["result"] = {"insertedId": None, "duplicate": True}
      res.status            = falcon.HTTP_200
    finally:
      client.close()
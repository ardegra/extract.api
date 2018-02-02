import pymongo
import falcon
import arrow

from lib.parser.AntaraOtoEntryDateParser import AntaraOtoEntryDateParser
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
      
      entry_date = article["entryDate"]
      if entry_date_parser == "AntaraOtoEntryDateParser":
        parser     = AntaraOtoEntryDateParser()
        entry_date = parser.parse(entry_date)
      elif entry_date_parser == "ArrowDateParser":
        parser     = ArrowDateParser()
        entry_date = parser.parse(entry_date)
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
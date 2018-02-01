import weblib
import falcon
import pymongo

from grab import Grab

class ExtractFirstPostId:
  def on_post(self, req, res):
    doc   = req.context["doc"]
    url   = doc["url"]
    xpath = doc["xpath"]
    
    print("[ExtractFirstPostId] url: {}".format(url))

    grab   = Grab()
    page   = grab.go(url)
    client = pymongo.MongoClient("mongodb://35.187.233.55:27017/ardegra")
  
    try:
      first_post_id_item = page.select(xpath["post"]["firstPostId"])
      first_post_id      = first_post_id_item.text()
      
      db        = client["ardegra"]
      document  = db["mention"].find_one({"id": first_post_id})
      duplicate = False if document is None else True
    except weblib.error.DataNotFound:
      first_post_id = None
      duplicate     = None
    finally:
      client.close()

    res.context["result"] = {"firstPostId": first_post_id, "duplicate": duplicate}
    res.status            = falcon.HTTP_200
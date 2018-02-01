import pymongo
import falcon

class NewsInfoIsArticleDuplicate:
  def on_post(self, req, res):
    doc = req.context["doc"]
    url = doc["url"]
    
    client = pymongo.MongoClient("mongodb://35.187.233.55:27017/ardegra")
    try:
      print("[NewsInfoIsArticleDuplicate] checking url: {}".format(url))
      db        = client["ardegra"]
      document  = db.mention.find_one({"permalink": url})
      duplicate = True if document is not None else False
      
      res.context["result"] = {"duplicate": duplicate, "error": {"message": "success", "code": 200}}
      res.status            = falcon.HTTP_200
    except Exception as err:
      res.context["result"] = {"error": {"message": str(err), "code": 404}}
      res.status            = falcon.HTTP_404
    finally:
      client.close()
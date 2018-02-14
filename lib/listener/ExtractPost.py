import sys

import weblib
import falcon

from raven import Client
from logbook import Logger, StreamHandler
from grab import Grab

class ExtractPost:
  """ ExtractPost """
  def on_post(self, req, res):
    """ handles POST request """
    doc          = req.context["doc"]
    xpath        = doc["xpath"]
    url          = doc["url"]
    
    raven_client = Client()
    StreamHandler(sys.stdout).push_application()
    logger = Logger("ExtractPost")
    
    logger.debug("url: {}".format(url))
    
    try:
      grab = Grab()
      page = grab.go(url)
      
      result = {"postList": []}
      
      post_items = page.select(xpath["post"]["item"])
      logger.debug("post_items: {}".format(len(post_items)))
      for index, post in enumerate(post_items):
        try:
          logger.debug("Post {} of {}".format(index + 1, len(post_items)))
          result["postList"].append({
            "id": post.select(xpath["post"]["id"]).text(),
            "entryDate": post.select(xpath["post"]["entryDate"]).text(),
            "content": post.select(xpath["post"]["content"]).text(),
            "permalink": grab.make_url_absolute(post.select(xpath["post"]["permalink"]).attr("href")),
            "authorId": post.select(xpath["post"]["authorId"]).text(),
            "authorName": post.select(xpath["post"]["authorName"]).text(),
            "authorUrl": grab.make_url_absolute(post.select(xpath["post"]["authorUrl"]).attr("href"))
          })
        except weblib.error.DataNotFound as err:
          raven_client.captureException()
          logger.error("{}".format(err))
          result["postList"].append({"error": str(err)})
    except Exception as err:
      raven_client.captureException()
      logger.error("{}".format(err))
      result["postList"].append({"error": str(err)})
    res.context["result"] = result
    res.status            = falcon.HTTP_200
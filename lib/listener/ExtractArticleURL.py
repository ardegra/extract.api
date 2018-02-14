import sys

import weblib
import falcon

from raven import Client
from logbook import Logger, StreamHandler
from grab import Grab

class ExtractArticleURL:
  """ ExtractArticleURL """
  def on_post(self, req, res):
    """ handle POST requests """
    doc          = req.context["doc"]
    xpath        = doc["xpath"]
    url          = doc["url"]
    
    raven_client = Client()
    StreamHandler(sys.stdout).push_application()
    logger = Logger("ExtractArticleURL")
    
    try:
      logger.debug("url: {}".format(url))
      grab = Grab()
      page = grab.go(url)
      
      result           = {"articleUrl": []}
      article_url_list = page.select(xpath["article"]["url"])
      for index, article_url in enumerate(article_url_list):
        logger.debug("Article URL: {} of {}".format(index, len(article_url_list)))
        
        article_url = article_url.attr("href")
        article_url = grab.make_url_absolute(article_url, resolve_base=True)
        
        logger.debug("article_url: {}".format(article_url))
        result["articleUrl"].append(article_url)
    except Exception as err:
      raven_client.captureException()
      logger.error(str(err))
      raise falcon.HTTPBadRequest("Ops! Something wrong", str(err))
    res.context["result"] = result
    res.status            = falcon.HTTP_200
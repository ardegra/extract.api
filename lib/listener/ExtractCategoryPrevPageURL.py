""" ExtractCategoryPrevPageURL """
import sys

import weblib
import falcon

from raven import Client
from logbook import Logger, StreamHandler
from grab import Grab

class ExtractCategoryPrevPageURL:
  """ ExtractCategoryPrevPageURL """
  def on_post(self, req, res):
    """ handles POST request """
    doc          = req.context["doc"]
    url          = doc["url"]
    xpath        = doc["xpath"]
    
    raven_client = Client()
    StreamHandler(sys.stdout).push_application()
    logger = Logger("ExtractCategoryPrevPageURL")
    
    try:
      logger.debug("url: {}".format(url))
      grab = Grab()
      page = grab.go(url)
      
      prev_page_item = page.select(xpath["category"]["prevPage"])
      prev_page_url  = prev_page_item.attr("href")
      prev_page_url  = grab.make_url_absolute(prev_page_url, resolve_base=True)
      logger.debug("prev_page_url: {}".format(prev_page_url))
    except Exception as err:
      raven_client.captureException()
      logger.error(str(err))
      prev_page_url = None
    
    res.context["result"] = {"prevPageUrl": prev_page_url}
    res.status            = falcon.HTTP_200
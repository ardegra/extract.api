import sys

import weblib
import falcon

from raven import Client
from logbook import Logger, StreamHandler
from grab import Grab

class ExtractThreadLastPageURL:
  def on_post(self, req, res):
    """ handles POST requests """
    doc          = req.context["doc"]
    url          = doc["url"]
    xpath        = doc["xpath"]
    
    raven_client = Client()
    StreamHandler(sys.stdout).push_application()
    logger = Logger("ExtractThreadLastPageURL")
    
    try:
      logger.debug("url: {}".format(url))
      grab = Grab()
      page = grab.go(url)
      
      last_page_item = page.select(xpath["thread"]["lastPage"])
      last_page_url  = grab.make_url_absolute(last_page_item.attr("href"), resolve_base=True)
      logger.debug("last_page_url: {}".format(last_page_url))
    except Exception as err:
      raven_client.captureException()
      logger.error(str(err))
      last_page_url = None
    res.context["result"] = {"lastPageUrl": last_page_url}
    res.status            = falcon.HTTP_200
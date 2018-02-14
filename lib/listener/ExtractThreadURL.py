import sys

import falcon

from raven import Client
from logbook import Logger, StreamHandler
from grab import Grab

class ExtractThreadURL:
  """ ExtractThreadURL """
  def on_post(self, req, res):
    """ handles POST requests """
    doc          = req.context["doc"]
    xpath        = doc["xpath"]
    url          = doc["url"]
    
    raven_client = Client()
    StreamHandler(sys.stdout).push_application()
    logger = Logger("ExtractThreadURL")
    
    try:
      logger.debug("url: {}".format(url))
      grab = Grab()
      page = grab.go(url)
          
      result           = {"threadList": []}
      thread_url_items = page.select(xpath["thread"]["url"])
      for index, thread_url in enumerate(thread_url_items):
        logger.debug("Thread URL: {} of {}".format(index + 1, len(thread_url_items)))
        
        thread_url = thread_url.attr("href")
        thread_url = grab.make_url_absolute(thread_url, resolve_base=True)
        
        logger.debug("Thread URL {}".format(thread_url))
        result["threadList"].append(thread_url)
    except Exception as ex:
      raven_client.captureException()
      logger.error(str(ex))
      result = {"threadList": []}
    res.context["result"] = result
    res.status            = falcon.HTTP_200
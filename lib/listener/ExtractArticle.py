import sys
import json

import weblib
import falcon

from raven import Client
from logbook import Logger, StreamHandler
from grab import Grab

class ExtractArticle:
  """ ExtractArticle """
  def on_post(self, req, res):
    """ handle POST request """
    doc          = req.context["doc"]
    xpath        = doc["xpath"]
    url          = doc["url"]
    
    raven_client = Client()
    StreamHandler(sys.stdout).push_application()
    logger = Logger("ExtractArticle")
    
    try:
      logger.debug("url: {}".format(url))
      grab = Grab()
      page = grab.go(url)
      
      content      = page.select(xpath["article"]["content"])
      real_content = ""
      if len(content) > 1:
        for c in content:
          real_content = "{}{}".format(real_content, c.text())
      else:
        real_content = content.text()
      result = {
        "title": page.select(xpath["article"]["title"]).text(),
        "content": real_content,
        "entryDate": page.select(xpath["article"]["entryDate"]).text()
      }
      logger.debug("Extracted Article: {}".format(json.dumps(result)))
    except Exception as err:
      raven_client.captureException()
      logger.error(str(err))
      raise falcon.HTTPBadRequest("Ops! Something wrong", str(err))
    res.context["result"] = result
    res.status            = falcon.HTTP_200
  
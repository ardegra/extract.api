import weblib
import falcon

from grab import Grab

class ExtractArticle:
  """ ExtractArticle """
  def on_post(self, req, res):
    """ handle POST request """
    doc   = req.context["doc"]
    xpath = doc["xpath"]
    url   = doc["url"]
    
    print("[ExtractArticle] url: {}".format(url))
    
    grab = Grab()
    page = grab.go(url)
    
    try:
      result = {
        "title": page.select(xpath["article"]["title"]).text(),
        "content": page.select(xpath["article"]["content"]).text(),
        "entryDate": page.select(xpath["article"]["entryDate"]).text()
      }
    except weblib.error.DataNotFound as err:
      raise falcon.HTTPBadRequest("Ops! Something wrong", str(err))
    res.context["result"] = result
    res.status            = falcon.HTTP_200
  
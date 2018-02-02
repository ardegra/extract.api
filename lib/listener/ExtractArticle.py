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
      content      = page.select(xpath["article"]["content"])
      real_content = ""
      if len(content) > 1:
        for c in content:
          real_content = "{}{}".format(real_content, c.text())
      result = {
        "title": page.select(xpath["article"]["title"]).text(),
        "content": real_content,
        "entryDate": page.select(xpath["article"]["entryDate"]).text()
      }
    except weblib.error.DataNotFound as err:
      raise falcon.HTTPBadRequest("Ops! Something wrong", str(err))
    res.context["result"] = result
    res.status            = falcon.HTTP_200
  
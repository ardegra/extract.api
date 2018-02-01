import weblib
import falcon

from grab import Grab

class ExtractArticleURL:
  """ ExtractArticleURL """
  def on_post(self, req, res):
    """ handle POST requests """
    doc   = req.context["doc"]
    xpath = doc["xpath"]
    url   = doc["url"]
    
    print("[ExtractArticleURL] url: {}".format(url))
    
    grab = Grab()
    page = grab.go(url)
    
    try:
      result           = {"articleUrl": []}
      article_url_list = page.select(xpath["article"]["url"])
      for article_url in article_url_list:
        result["articleUrl"].append(article_url.attr("href"))
    except weblib.error.DataNotFound as err:
      raise falcon.HTTPBadRequest("Ops! Something wrong", str(err))
    res.context["result"] = result
    res.status            = falcon.HTTP_200
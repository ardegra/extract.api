""" ExtractCategoryPrevPageURL """
import weblib
import falcon

from grab import Grab

class ExtractCategoryPrevPageURL:
  """ ExtractCategoryPrevPageURL """
  def on_post(self, req, res):
    """ handles POST request """
    doc   = req.context["doc"]
    url   = doc["url"]
    xpath = doc["xpath"]
    
    print("[ExtractCategoryPrevPageURL] url: {}".format(url))
    
    grab = Grab()
    page = grab.go(url)
    
    try:
      prev_page_item = page.select(xpath["category"]["prevPage"])
      prev_page_url  = grab.make_url_absolute(prev_page_item.attr("href"))
    except weblib.error.DataNotFound:
      prev_page_url = None
    
    res.context["result"] = {"prevPageUrl": prev_page_url}
    res.status            = falcon.HTTP_200
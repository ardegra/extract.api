import weblib
import falcon

from grab import Grab

class ExtractThreadLastPageURL:
  def on_post(self, req, res):
    """ handles POST requests """
    doc   = req.context["doc"]
    url   = doc["url"]
    xpath = doc["xpath"]
    
    print("[ExtractThreadLastPageURL] url: {}".format(url))
    
    grab = Grab()
    page = grab.go(url)
    
    try:
      last_page_item = page.select(xpath["thread"]["lastPage"])
      last_page_url  = grab.make_url_absolute(last_page_item.attr("href"))
    except weblib.error.DataNotFound:
      last_page_url = None

    res.context["result"] = {"lastPageUrl": last_page_url}
    res.status            = falcon.HTTP_200
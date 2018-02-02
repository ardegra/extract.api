import weblib
import falcon

from grab import Grab

class ExtractThreadPrevPageURL:
  def on_post(self, req, res):
    doc   = req.context["doc"]
    url   = doc["url"]
    xpath = doc['xpath']
    
    print("[ExtractThreadPrevPageURL] url: {}".format(url))
    
    grab = Grab()
    page = grab.go(url)
    
    try:
      prev_page_item = page.select(xpath["thread"]["prevPage"])
      prev_page_url  = grab.make_url_absolute(prev_page_item.attr("href"), resolve_base=True)
    except weblib.error.DataNotFound:
      prev_page_url = None
  
    res.context["result"] = {"prevPageUrl": prev_page_url}
    res.status            = falcon.HTTP_200
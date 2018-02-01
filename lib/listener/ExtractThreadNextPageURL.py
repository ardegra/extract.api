import weblib
import falcon

from grab import Grab
class ExtractThreadNextPageURL:
  def on_post(self, req, res):
    doc   = req.context["doc"]
    url   = doc["url"]
    xpath = doc["xpath"]
    
    print("[ExtractThreadNextPageURL] url: {}".format(url))

    grab = Grab()
    page = grab.go(url)

    try:
      next_page_item = page.select(xpath["thread"]["nextPage"])
      next_page_url  = grab.make_url_absolute(next_page_item.attr("href"))
    except weblib.error.DataNotFound:
      next_page_url = None

    res.context["result"] = {"nextPageUrl": next_page_url}
    res.status            = falcon.HTTP_200

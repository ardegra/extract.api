""" ExtractLExtractCategoryLastPageURLastPageURL """
import falcon

from grab import Grab

class ExtractCategoryLastPageURL:
  """ ExtractCategoryLastPageURL """
  def on_post(self, req, res):
    """ handles POST requests """
    doc   = req.context["doc"]
    url   = doc["url"]
    xpath = doc["xpath"]
    
    print("[ExtractCategoryLastPageURL] url: {}".format(url))
    
    grab = Grab()
    page = grab.go(url)
    
    last_page_item = page.select(xpath["category"]["lastPage"])
    print("[ExtractCategoryLastPageURL] item type: {}".format(type(last_page_item)))
    
    last_page_url  = grab.make_url_absolute(last_page_item.attr("href"))
    result         = {"lastPageUrl": last_page_url}
    
    res.context["result"] = result
    res.status            = falcon.HTTP_200
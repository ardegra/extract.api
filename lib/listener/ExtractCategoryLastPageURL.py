""" ExtractLExtractCategoryLastPageURLastPageURL """
import falcon
import weblib

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
    
    try:
      last_page_item = page.select(xpath["category"]["lastPage"])
      last_page_url  = last_page_item.attr("href")
      
      if not "http://" in last_page_url:
        if last_page_url[0] != "/":
          last_page_url = "/{}".format(last_page_url)
      
      print("[ExtractCategoryLastPageURL] last_page_url: {}".format(last_page_url))
      last_page_url  = grab.make_url_absolute(last_page_item.attr("href"), resolve_base=True)
      result         = {"lastPageUrl": last_page_url}
    except weblib.error.DataNotFound as err:
      result = {"lastPageUrl": None, "error": {"message": str(err), "code": 404}}
    res.context["result"] = result
    res.status            = falcon.HTTP_200
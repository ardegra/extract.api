import falcon

from grab import Grab

class ExtractThreadURL:
  """ ExtractThreadURL """
  def on_post(self, req, res):
    """ handles POST requests """
    doc   = req.context["doc"]
    xpath = doc["xpath"]
    url   = doc["url"]
    
    print("[ExtractThreadURL] url: {}".format(url))
    
    grab = Grab()
    page = grab.go(url)
        
    result           = {"threadList": []}
    thread_url_items = page.select(xpath["thread"]["url"])
    for thread_url in thread_url_items:
      result["threadList"].append(grab.make_url_absolute(thread_url.attr("href")))
    res.context["result"] = result
    res.status            = falcon.HTTP_200
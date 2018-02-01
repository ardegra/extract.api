import weblib
import falcon

from grab import Grab

class ExtractPost:
  """ ExtractPost """
  def on_post(self, req, res):
    """ handles POST request """
    doc   = req.context["doc"]
    xpath = doc["xpath"]
    url   = doc["url"]
    
    print("[ExtractPost] url: {}".format(url))
    
    grab = Grab()
    page = grab.go(url)
    
    result = {"postList": []}
    
    post_items = page.select(xpath["post"]["item"])
    for post in post_items:
      try:
        result["postList"].append({
          "id": post.select(xpath["post"]["id"]).text(),
          "entryDate": post.select(xpath["post"]["entryDate"]).text(),
          "content": post.select(xpath["post"]["content"]).text(),
          "permalink": grab.make_url_absolute(post.select(xpath["post"]["permalink"]).attr("href")),
          "authorId": post.select(xpath["post"]["authorId"]).text(),
          "authorName": post.select(xpath["post"]["authorName"]).text(),
          "authorUrl": grab.make_url_absolute(post.select(xpath["post"]["authorUrl"]).attr("href"))
        })
      except weblib.error.DataNotFound:
        result["postList"].append({})
    res.context["result"] = result
    res.status            = falcon.HTTP_200
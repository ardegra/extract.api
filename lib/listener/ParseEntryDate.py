import falcon

from lib.parser.ParseEntryDate import ParseEntryDate as PED

class ParseEntryDate:
  def on_post(self, req, res):
    doc    = req.context["doc"]
    parser = doc["parser"]
    date   = doc["date"]
    
    error = {"status": {"code": 200, "message": "success"}}
    try:
      date = PED.parse(parser, date)
    except Exception as ex:
      date = None
      error = {"status": {"code": 200, "message": str(ex)}}
    res.context["result"] = { "parsedDate": date, "error": error}
    res.status            = falcon.HTTP_200
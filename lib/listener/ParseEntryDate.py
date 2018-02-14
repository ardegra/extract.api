import sys

import falcon

from lib.parser.ParseEntryDate import ParseEntryDate as PED

from raven import Client
from logbook import Logger, StreamHandler

class ParseEntryDate:
  def on_post(self, req, res):
    doc          = req.context["doc"]
    parser       = doc["parser"]
    date         = doc["date"]
    
    raven_client = Client()
    StreamHandler(sys.stdout).push_application()
    logger = Logger("ParseEntryDate")
    
    logger.debug("parser_name: {}".format(parser))
    
    error = {"status": {"code": 200, "message": "success"}}
    try:
      date = PED.parse(parser, date)
    except Exception as ex:
      raven_client.captureException()
      logger.error(str(ex))
      date = None
      error = {"status": {"code": 200, "message": str(ex)}}
    res.context["result"] = { "parsedDate": date, "error": error}
    res.status            = falcon.HTTP_200
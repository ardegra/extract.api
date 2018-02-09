import falcon

from lib.parser.AntaraOtoEntryDateParser import AntaraOtoEntryDateParser
from lib.parser.ArrowDateParser import ArrowDateParser
from lib.parser.AjnnEntryDateParser import AjnnEntryDateParser
from lib.parser.DetikOtoEntryDateParser import DetikOtoEntryDateParser
from lib.parser.KoranJakartaEntryDateParser import KoranJakartaEntryDateParser
from lib.parser.MedcomEntryDateParser import MedcomEntryDateParser
from lib.parser.TempoEntryDateParser import TempoEntryDateParser

class ParseEntryDate:
  def on_post(self, req, res):
    doc    = req.context["doc"]
    parser = doc["parser"]
    date   = doc["date"]
    
    error = {"status": {"code": 200, "message": "success"}}
    try:
      if parser == "AntaraOtoEntryDateParser":
        parser = AntaraOtoEntryDateParser()
      elif parser == "ArrowDateParser":
        parser = ArrowDateParser()
      elif parser == "Ajnn":
        parser = AjnnEntryDateParser()
      elif parser == "DetikOtoEntryDateParser":
        parser = DetikOtoEntryDateParser()
      elif parser == "KoranJakartaEntryDateParser":
        parser = KoranJakartaEntryDateParser()
      elif parser == "MedcomEntryDateParser":
        parser = MedcomEntryDateParser()
      elif parser == "TempoEntryDateParser":
        parser = TempoEntryDateParser()
        
      date = parser.parse(date)
      date = date.isoformat()
    except Exception as ex:
      date = None
      error = {"status": {"code": 200, "message": str(ex)}}
    res.context["result"] = { "parsedDate": date, "error": error}
    res.status            = falcon.HTTP_200
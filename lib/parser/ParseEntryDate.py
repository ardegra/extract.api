from lib.parser.AntaraOtoEntryDateParser import AntaraOtoEntryDateParser
from lib.parser.ArrowDateParser import ArrowDateParser
from lib.parser.AjnnEntryDateParser import AjnnEntryDateParser
from lib.parser.DetikOtoEntryDateParser import DetikOtoEntryDateParser
from lib.parser.KoranJakartaEntryDateParser import KoranJakartaEntryDateParser
from lib.parser.MedcomEntryDateParser import MedcomEntryDateParser
from lib.parser.TempoEntryDateParser import TempoEntryDateParser
from lib.parser.TestingParser import TestingParser

class ParseEntryDate:
  @staticmethod
  def parse(parser, date):
    if parser == "AntaraOtoEntryDateParser":
      parser = AntaraOtoEntryDateParser()
    elif parser == "ArrowDateParser":
      parser = ArrowDateParser()
    elif parser == "AjnnEntryDateParser":
      parser = AjnnEntryDateParser()
    elif parser == "DetikOtoEntryDateParser":
      parser = DetikOtoEntryDateParser()
    elif parser == "KoranJakartaEntryDateParser":
      parser = KoranJakartaEntryDateParser()
    elif parser == "MedcomEntryDateParser":
      parser = MedcomEntryDateParser()
    elif parser == "TempoEntryDateParser":
      parser = TempoEntryDateParser()
    elif parser == "TestingParser":
      parser = TestingParser()
    date = parser.parse(date)
    date = date.isoformat()
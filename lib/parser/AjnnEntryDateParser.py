import arrow

from lib.parser.IndonesiaDateParser import IndonesiaDateParser

class AjnnEntryDateParser:
  def parse(self, entry_date):
    # 2017-09-20 15:01:11
    entry_date = entry_date.split("-")
    date       = entry_date[2]
    month      = entry_date[1]
    year       = entry_date[0]
    
    full_date = "{}-{}-{}T00:00:00.000Z".format(year, month, date)
    full_date = arrow.get(full_date).datetime
    return full_date
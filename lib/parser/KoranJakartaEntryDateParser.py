import arrow

from lib.parser.IndonesiaDateParser import IndonesiaDateParser

class KoranJakartaEntryDateParser:
  def parse(self, entry_date):
    # Jumat 9/2/2018 | 06:21
    splits = entry_date.split(" ")
    entry_date = splits[1].split("/")
    date       = str(entry_date[0]).zfill(2)
    month      = str(entry_date[1]).zfill(2)
    year       = entry_date[2]
    
    full_date = "{}-{}-{}T00:00:00.000Z".format(year, month, date)
    full_date = arrow.get(full_date).datetime
    return full_date
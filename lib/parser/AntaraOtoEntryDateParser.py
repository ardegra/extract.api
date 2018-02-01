import arrow

from lib.parser.IndonesiaDateParser import IndonesiaDateParser

class AntaraOtoEntryDateParser:
  def parse(self, entry_date):
    entry_date = entry_date.split(",")[1]
    entry_date = entry_date.split(" ")
    
    print("[AntaraOtoEntryDateParser] {}".format(entry_date))
    date  = entry_date[1].zfill(2)
    month = IndonesiaDateParser.parse_month_to_number(entry_date[2])
    year  = entry_date[3]
    
    full_date = "{}-{}-{}T00:00:00.000Z".format(year, month, date)
    print("[AntaraOtoEntryDateParser] {}".format(full_date))
    
    full_date = arrow.get(full_date).datetime
    return full_date
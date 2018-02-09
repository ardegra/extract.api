import arrow

from lib.parser.IndonesiaDateParser import IndonesiaDateParser

class MedcomEntryDateParser:
  def parse(self, entry_date):
    # 09 Februari 2018 10:20 WIB
    entry_date = entry_date.split(" ")
    date       = entry_date[0]
    month      = IndonesiaDateParser.parse_month_to_number(entry_date[1])
    year       = entry_date[2]
    
    full_date = "{}-{}-{}T00:00:00.000Z".format(year, month, date)
    full_date = arrow.get(full_date).datetime
    return full_date
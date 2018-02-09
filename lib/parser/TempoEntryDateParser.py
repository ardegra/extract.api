import arrow

from lib.parser.IndonesiaDateParser import IndonesiaDateParser

class TempoEntryDateParser:
  def parse(self, entry_date):
    # Jumat, 2 Februari 2018 21:26 WIB
    entry_date = entry_date.split(" ")
    date       = str(entry_date[1]).zfill(2)
    month      = IndonesiaDateParser.parse_month_to_number(entry_date[2])
    year       = entry_date[3]
    
    full_date = "{}-{}-{}T00:00:00.000Z".format(year, month, date)
    full_date = arrow.get(full_date).datetime
    return full_date
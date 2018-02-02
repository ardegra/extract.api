class DetikOtoEntryDateParser:
  def parse(self, entry_date):
    # Jumat 02 Februari 2018, 15:44 WIB
    entry_date = entry_date.split(" ")
    date       = entry_date[1]
    month      = entry_date[2]
    year       = entry_date[3]
    
    full_date = "{}-{}-{}T00:00:00.000Z".format(year, month, date)
    full_date = arrow.get(full_date).datetime
    return full_date
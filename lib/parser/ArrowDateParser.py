import arrow

class ArrowDateParser:
  def parse(self, entry_date):
    return arrow.get(entry_date).to("utc").datetime

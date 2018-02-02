import arrow

class ArrowDateParser:
  def parse(self, date):
    return arrow.get(date).to("utc").datetime
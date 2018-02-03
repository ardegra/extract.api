class IndonesiaDateParser:
  
  @staticmethod
  def parse_month_to_number(month):
    month = month.lower()
    if month == "januari" or month == "january":
      return "01"
    elif month == "februari" or month == "febuari" or month == "february":
      return "02"
    elif month == "maret" or month == "march":
      return "03"
    elif month == "april":
      return "04"
    elif month == "mei" or month == "may":
      return "05"
    elif month == "juni" or month == "june":
      return "06"
    elif month == "juli" or month == "july":
      return "07"
    elif month == "agustus" or month == "august":
      return "08"
    elif month == "september":
      return "09"
    elif month == "oktober" or month == "october":
      return "10"
    elif month == "nopember" or month == "november":
      return "11"
    elif month == "desember" or month == "december":
      return "12"
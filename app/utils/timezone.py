from pytz import timezone, utc

def convert_ist_to_utc(dt):
    ist = timezone("Asia/Kolkata")
    return ist.localize(dt).astimezone(utc)

def convert_utc_to_ist(dt):
    ist = timezone("Asia/Kolkata")
    return dt.astimezone(ist)

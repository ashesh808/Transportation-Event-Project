import re
from datetime import timedelta

class DateTimeHelper:
    def seconds_to_hms(s):
        try:
            seconds = int(s)
        except ValueError:
            return "Invalid Time Format"
        return str(timedelta(seconds=seconds))

    def hms_to_seconds(t):
        h, m, s = re.split('[:.]', t)
        return int(h) * 3600 + int(m) * 60 + int(s) 
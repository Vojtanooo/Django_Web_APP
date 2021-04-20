import datetime


def get_month(dt):
    month_list = ["LEDEN", "ÚNOR", "BŘEZEN", "DUBEN",
                  "KVĚTEN", "ČERVEN", "ČERVENEC", "SRPEN",
                  "ZÁŘÍ", "ŘÍJEN", "LISTOPAD", "PROSINEC"]
    return month_list.index(dt)


def get_total_hours(list_of_items):
    total_h = [item.result for item in list_of_items]
    total_hours = datetime.timedelta()
    for i in total_h:
        (h, m, s) = i.split(':')
        d = datetime.timedelta(
            hours=int(h), minutes=int(m), seconds=int(s))
        total_hours += d
    return (total_hours.total_seconds() / 3600)


def get_strp_time(number_start, number_end):
    strp_start = datetime.datetime.strptime(number_start, "%H:%M")
    strp_end = datetime.datetime.strptime(number_end, "%H:%M")

    if number_start == "00:00" and number_end == "00:00":
        return "24:00:00"
    elif number_end == "00:00" or number_end == "23:59":
        strp_end = datetime.datetime.strptime("00:00", "%H:%M")
        return (strp_end + datetime.timedelta(days=1)) - strp_start
    else:
        return strp_end - strp_start


def get_month_name_czech():
    month_list = ["LEDEN", "ÚNOR", "BŘEZEN", "DUBEN",
                  "KVĚTEN", "ČERVEN", "ČERVENEC", "SRPEN",
                  "ZÁŘÍ", "ŘÍJEN", "LISTOPAD", "PROSINEC"]
    now = datetime.datetime.today()
    get_month = now.month
    return month_list[get_month - 1]

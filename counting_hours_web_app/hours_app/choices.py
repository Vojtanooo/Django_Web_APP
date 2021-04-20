from .models import Day
import json
import datetime


def choice(user):
    obj = Day.objects.filter(author=user)
    obj_list = [item.working_day.split("-")[0].strip() for item in obj]
    dt = datetime.datetime.now().month - 1

    DAYS_IN_MONTH = days()[dt]
    for i in obj_list:
        for x in DAYS_IN_MONTH:
            if i == x[0]:
                DAYS_IN_MONTH.remove(x)

    return DAYS_IN_MONTH


def days():
    print("OPEN JSON")
    with open("year_month_database.json") as file:
        data = json.load(file)
        return data

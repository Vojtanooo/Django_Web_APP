from bs4 import BeautifulSoup as bs
import requests
import datetime
import json


def main():
    all_items = get_days()
    with open("year_month_database.json", "w") as txt_file:
        json.dump(all_items, txt_file, sort_keys=True, indent=1)


def get_days():
    list_of_all_data = []
    for num in range(1, 13):
        list_of_tuples = []
        url_link = f"https://kalendar.beda.cz/2021-{num}?"
        raw_html = get_request(url_link)
        bs4_text = parsing_html(raw_html.text)
        days = get_days_month(bs4_text)
        number_name = get_number_name(days[0])
        list_of_tuples = [(f"{item}.{days[1]}", f"{item}.{days[1]}")
                          for item in number_name]
        list_of_all_data.append(list_of_tuples)
    return list_of_all_data


def get_request(url):
    with requests.Session() as req:
        return req.get(url)


def parsing_html(html):
    return bs(html, "html.parser")


def get_days_month(bs4):
    table = bs4.find("table", id="month")
    days = table.findAll("tr")[2:7]
    month = table.find("tr")
    return days, month.text.strip().replace(u'\xa0\xa0', u' ')


def get_number_name(tr):
    full_list = []
    for item in tr:
        full_list.extend(item.findAll("td", {"class": "normal"}))
    full_list = [item.find("div", {"class": "big"}).text
                 for item in full_list]
    return full_list


main()

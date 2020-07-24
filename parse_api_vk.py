import csv
import os

import requests
from bs4 import BeautifulSoup as BS

filename = input("Название файла : ")
path = "result/" + filename + ".csv"
token = 'dcc6e61edcc6e61edcc6e61e54dcb5c83dddcc6dcc6e61e83dc38c74da087ddea748480'
version = '5.120'
domain = "yvkurse"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 OPR/69.0.3686.77",
    "accept": "*/*"
}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def all_posts():
    global all_data
    response = requests.get("https://api.vk.com/method/wall.get",
                            params={
                                "access_token": token,
                                "v": version,
                                "domain": domain,
                                "count": 100
                            }
                            )
    all_data = response.json()["response"]["items"]


def save_file(items, path=path):
    with open(path, "w", newline="", encoding="utf16")as file:
        writter = csv.writer(file, delimiter="\t")
        writter.writerow(["Заголовок", "Текст", "текст статьи", "Картинка", "Ссылка"])
        for item in items:
            if item['attachments'][0]["type"] == "link":
                url = item["attachments"][0]["link"]["url"]
                html = get_html(url)
                soup = BS(html.text, "html.parser")
                bitems = soup.find_all("div", class_="article article_view article_mobile")
                info = ""
                for bitem in bitems:
                    try:
                        b = bitem.find("p",
                                       class_="article_decoration_first article_decoration_last article_decoration_before").get_text()
                        info = b
                    except AttributeError:
                        pass
                writter.writerow(
                    [item['attachments'][0]["link"]["title"], item["text"], info,
                     item['attachments'][0]["link"]["photo"]["sizes"][0]["url"], item["attachments"][0]["link"]["url"]])
            else:
                pass


def parse():
    all_posts()
    save_file(all_data)
    os.startfile(r"result\{}".format(filename+".csv"))


parse()

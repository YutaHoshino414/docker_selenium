import requests
import rich
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parse():
    base = "https://www.keiostore.co.jp/business/store_list.html"
    res = requests.get(base)
    sp = BeautifulSoup(res.content, 'html.parser')
    for url in [urljoin(base,a.get('href')) for a in sp.select('td.storeName a')]:
        yield url

def collect(url):
    columns = ["住所", "電話番号", "FAX番号", "営業時間", "アクセス", "駐車場", "取扱品目"]
    datas = dict.fromkeys(columns, "")
    res = requests.get(url)
    sp = BeautifulSoup(res.content, 'html.parser')
    datas["店舗名"] = sp.select_one("h2").text
    for th in columns:
        if column := sp.select(f"th:-soup-contains('{th}')~td"):
            datas[th] = column[0].text
    return datas


if __name__ == '__main__':
    for result in map(collect, parse()):
        with open("results.jl", "a") as f:
            print(result, file=f)
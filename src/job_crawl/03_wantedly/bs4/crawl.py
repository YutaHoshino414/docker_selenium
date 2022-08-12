import csv
import datetime
import json
import math
import re
import requests
from bs4 import BeautifulSoup
from time import sleep
from urllib.parse import urljoin, unquote


class BsParser:
    def __init__(self):
        self.url = "https://www.wantedly.com/projects?type=mixed&page=1&occupation_types[]=jp__engineering&hiring_types[]=mid_career&hiring_types[]=side_job&company_tags[]=overseas"
        self.request_url(self.url)
        # start url
        self.data = {}
        self.date = datetime.date.today()

    def request_url(self, url):
        self.res = requests.get(url) ;sleep(2)
        if self.res.status_code == 200:
            self.soup = BeautifulSoup(self.res.content, "html.parser")
        return self.soup
    
    def fetch(self):
        result = int(self.soup.select_one('span.total').text)
        pages = math.ceil(result/10)
        print(f"result:::{result}\npages:::{pages}")
        i = 0
        for page in range(pages):
            print(page)
            sp = self.request_url(f"{self.url}&page={page+1}")
            for a in sp.select('div.project-index-single-inner h1 a'):
                self.data['id'] = i
                self.data['url'] = re.sub(r'\?.+','', urljoin(self.url, a.get('href')))
                self.data['title'] = a.text
                print(self.data, sep="\n")
                self.output_csv(self.data.values())
                i += 1
    
    
    def output_csv(self, data:[]):
        with open(f'./{self.date}.csv', 'a') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(data)
    
    def output_json(self):
        with open('../datas/results.jsonlines', 'a') as f:
            print(self.data, file=f)


if __name__ == '__main__':
    sp = BsParser()
    sp.fetch()
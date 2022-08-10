import csv
import datetime
import math
import re
import rich
import schedule
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
from urllib.parse import unquote

class Crawler:
    def __init__(self):
        options = Options()
        #options.add_argument('--headless')  
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        self.today = datetime.date.today()
        # start url
        self.URL = 'https://stores.welcia.co.jp/index.html'
        
    def page_open(self, url):
        self.driver.execute_script(f"window.open('{url}')")
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def page_close(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def main(self):
        """再帰呼び出しによる巡回"""
        # 県・市・区町村ごとに階層が深くなるが、同様のサイト構成で深くなっているパターンのサイトに応用できる
        def recursive_search(url, step):
            print(unquote(url))
            self.page_open(url)
            if links := self.driver.find_elements_by_xpath('//ul[@class="Directory-listLinks"]/li/a'):
                for area_url in [a.get_attribute("href") for a in links]:
                    if re.search(r'\d{1,4}D', area_url):
                        collect(area_url)
                    else:
                        recursive_search(area_url, step + 1)
            else:
                for tenpo in [a.get_attribute("href") for a in self.driver.find_elements_by_xpath('//li[@class="Directory-listTeaser"]//h2/a')]:
                    collect(tenpo)
            self.page_close()

        def collect(url):
            print(unquote(url))
        
        step = 1
        recursive_search(self.URL, step)
    
    def output_csv(self, data:[]):
        with open(f'./{self.today}.csv', 'a') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(data)
    
    def output_json(self):
        with open('../datas/results.jsonlines', 'a') as f:
            print(self.data, file=f)


if __name__ == '__main__':
    crawler = Crawler()
    crawler.main()
    


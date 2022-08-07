""" 
会社名で重複するものは、除く（複数職種を出している） 

"""

import csv
import datetime
import math
import rich
import schedule
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm


class Crawler:
    def __init__(self):
        options = Options()
        #options.add_argument('--headless')  
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        self.today = datetime.date.today()
        # start url
        self.URL = 'https://www.wantedly.com/projects?type=mixed&locations[]=kanto&keywords[]=アルバイト&occupation_types[]=jp__engineering'
        
    def page_open(self, url):
        self.driver.execute_script(f"window.open('{url}')")
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def page_close(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])

def read_csv():
    today = datetime.date.today()

    with open(f'../{today}.csv', 'r') as f:
        lines = [line.split(',') for line in f.readlines()]
    check_dict = {}
    for line in lines[1:]:
        #rich.print(line); sleep(1)
        if check_dict.get(line[3]):
            continue
        check_dict[line[3]] = line[5]
    # 117 / 358件(2022-08-07) : 1/3は減った。
    print(len(check_dict))
    for url in [v.strip("\n") for v in check_dict.values()]:
        print(repr(url))
        crawler = Crawler()
        crawler.driver.get(url); sleep(2)



if __name__ == '__main__':
    read_csv()
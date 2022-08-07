import os
import csv
import re
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import datetime
from rich.traceback import install

class Crawler:
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument('--lang=ja')
        options.add_argument('--window-size=1000,1000')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        self.data = {}
        self.today = datetime.date.today()
        #install()
    
    def __del__(self):
        #self.driver.quit()
        del self.driver

    def crawl_main(self):  
        self.driver.get('https://baito.mynavi.jp/tokyo/ss-6/')
        sleep(2)
        for i, h2 in enumerate(self.driver.find_elements_by_xpath('//h2[@class="shopName"]')):
            if "マンパワー" in h2.text or "ヒューマン" in h2.text:
                continue
            company = h2.text
            link = h2.find_element_by_xpath('../following-sibling::div/div[@class="informationTextWrap"]/a')
            url = link.get_attribute('href')
            title = link.text
            #print(company, url)
            self.output_csv([i, company, url, title])
            #self.output_json()
        
        self.driver.close()
    
    def output_csv(self, data):
        with open(f'./{self.today}.csv', 'a') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(data)
    
    def output_json(self):
        with open('../datas/results.jsonlines', 'a') as f:
            print(self.data, file=f)


if __name__ == '__main__':
    crawler = Crawler()
    crawler.crawl_main()
    print(f'---------\n{crawler.today}: Task Done\n---------')
    del crawler
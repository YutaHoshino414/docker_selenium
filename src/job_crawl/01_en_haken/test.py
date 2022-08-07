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
        self.driver.get('https://haken.en-japan.com/kanto/list_wish/?signup=0&apply=1&visit=0&subapply=0&subvisit=0&CatID=F1131010,F1131020,F1131030,F1131040,F1131050,F1131060,F1131070,F1131080,F1131090,F1131100,F1131110,F1131120,F1131130,F1131140,F1131150,F1131160,F1131170,F1131180,F1131190,F1131200,F1131210,F1131220,F1131230,F1139010,F1139020,F1139030,F1139040,F1139050,F1139060,F1139070,F1139080,F1139090,F1139100,F1139110,F1139120,F1139130,F1139140,F1139150,F1139160,F1139170,F1139180,F1139190,F1139200,F1139210,F1139220,F1139230,F1139240,F1139250,F1139260,F1139990&PlaceType=1&jobtypeidList=D0301010,D0301020,D0301030,D0390900,D0401010,D0401020,D0401030,D0402010,D0403010,D0404010,D0404020,D0404030,D0404040,D0490900&mllist=20000000000000000000000000000000000000000000000000000000000000000000000000000&sortType=11')
        sleep(2)
        for i, div in enumerate(self.driver.find_elements_by_xpath('//div[@class="jobNameArea"]')):
            title = div.text.replace(',','').split('\n')[0]
            url = div.find_element_by_xpath("div/h2/a").get_attribute('href')
            self.data['title'] = re.sub("！|／|＠|＊","/",title)
            self.data['url'] = url
            self.data['agency'] = div.find_element_by_xpath('./following-sibling::div/div/dl[@class="dataSet company"]/dd/a').text
            self.output_csv([i, title, url])
            
            #self.output_json()
        
        self.driver.close()
    
    def output_csv(self, data):
        with open(f'./results_{self.today}.csv', 'a') as f:
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
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
        options.add_argument('--headless')  
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

    def main(self):
        with open(f'./{self.today}.csv', 'a') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(["id", "entry_num", "tag", "company", "title", "url"])
        
        self.driver.get(self.URL);sleep(2)
        result = int(self.driver.find_element_by_xpath('//span[@class="total"]').text)
        pages = math.ceil(result/10)
        print(f"result:::{result}\npages:::{pages}")
        i = 0
        skip = 0
        for page in tqdm(range(pages)[:50]):
            page_url = f"{self.URL}&page={page + 1}"
            self.page_open(page_url); print(f'page >>{page}')
            print(f"skip:::{skip}") 
            for single in self.driver.find_elements_by_xpath('//div[@class="project-index-single-inner"]//h1/a'):
                title = single.text
                if "学生" in title or "卒" in title:
                    skip += 1
                    continue
                tag = single.find_element_by_xpath('../..//div[contains(@class,"project-tag small normal")]').text
                if "QA" in tag or "テス" in tag or "インフラ" in tag or "PHP" in tag or "卒" in tag:
                    skip += 1
                    continue
                
                if entry := single.find_elements_by_xpath('../..//div[@class="entry-count"]/div'):
                    entry_count = entry[0].text
                company = single.find_element_by_xpath('../../../following-sibling::div//h3').text
                url = single.get_attribute('href')
                
                i += 1
                self.output_csv([i, entry_count, tag, company, title, url])
            self.page_close()
        self.driver.quit()
    
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
    print(f'------------------\n{crawler.today}: Task Done!\n-------------------')


"""定期実行"""
#def task():
#    crawler = Crawler()
#    crawler.main()
#    print(f'------------------\n{self.now}: Task Done!\n-------------------')
#
#schedule.every(1).hours.do(task)
#
#if __name__ == '__main__':
#    while True:
#        schedule.run_pending()
#        sleep(1)
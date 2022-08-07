from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import rich
import schedule
from time import sleep

class Crawler:
    def __init__(self):
        options = Options()
        options.add_argument('--headless')  
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        self.URL = 'http://quotes.toscrape.com/tag/humor/'
        self.now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    def main(self):
        self.driver.get(self.URL)
        for quote in self.driver.find_elements_by_xpath('//div[@class="quote"]/span[@class="text"]'):
            with open(f"cron_auto_{self.now}.txt", "a") as f:
                print(quote.text, file=f)

        self.driver.quit()

def task():
    crawler = Crawler()
    crawler.main()
    print(f'------------------\n{self.now}: Task Done!\n-------------------')

schedule.every(1).hours.do(task)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        sleep(1)
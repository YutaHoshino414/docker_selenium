from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import rich


class Crawler:
    def __init__(self):
        options = Options()
        options.add_argument('--headless')  
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        self.URL = 'http://quotes.toscrape.com/tag/humor/'
        
    def main(self):
        self.driver.get(self.URL)
        for quote in self.driver.find_elements_by_xpath('//div[@class="quote"]/span[@class="text"]'):
            print(quote.text)

        self.driver.quit()

if __name__ == '__main__':
    crawler = Crawler()
    crawler.main() 
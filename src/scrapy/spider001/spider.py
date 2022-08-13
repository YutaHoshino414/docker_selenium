import scrapy
from scrapy.crawler import CrawlerProcess
#from scrapy.extensions.httpcache import DummyPolicy


class TestSpider(scrapy.Spider):
    name = 'singlemalts'

    def start_requests(self):
        yield scrapy.Request('https://www.thewhiskyexchange.com/c/40/single-malt-scotch-whisky?pg=1&psize=100&sort=pasc')

    def parse(self, response):
        products = response.css('li.product-grid__item')
        for item in products:
            yield {
                'name' : item.css('p.product-card__name::text').get().strip(' '),
                'meta' : item.css('p.product-card__meta::text').get(),
                'price' : item.css('p.product-card__price::text').get(),
            }
        
        for page in range(2, 26):
            yield(
                scrapy.Request(
                    f'https://www.thewhiskyexchange.com/c/40/single-malt-scotch-whisky?pg={page}&psize=100&sort=pasc',
                    callback=self.parse
                ))


process = CrawlerProcess(settings={
    'FEED_URI' : 'whisky.csv',
    'FEED_FORMAT': 'csv',
    "DOWNLOAD_DELAY": 2,
    # キャッシュを有効にする
    "HTTPCACHE_ENABLED": True,
    # キャッシュの有効期限 0は期限なし
    "HTTPCACHE_EXPIRATION_SECS": 60 * 60 * 24,  # 24h
})

process.crawl(TestSpider)
process.start()
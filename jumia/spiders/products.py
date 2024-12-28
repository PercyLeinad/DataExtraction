import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import JumiaItem
from itemloaders import ItemLoader
class ProductsSpider(CrawlSpider):
    name = "products"
    allowed_domains = ["www.jumia.co.ke"]
    start_urls = ["https://www.jumia.co.ke/smartphones/?page=50#catalog-listing"]

    rules = (
             Rule(LinkExtractor(restrict_css='article.prd._fb.col.c-prd a.core'),callback='parse_item',follow=False),
             Rule(LinkExtractor(restrict_xpaths='//a[@aria-label="Next Page"]'),follow=True)
             )

    def parse_item(self, response):
        loader = ItemLoader(selector=response,item=JumiaItem())

        loader.add_css('name','h1::text')
        loader.add_xpath('brand',"//div[contains(text(),'Brand')]/a[1]/text()")
        loader.add_xpath('new_price','//div[@class="-hr -mtxs -pvs"]/div/span/text()')
        loader.add_xpath('old_price','//div[@class="-hr -mtxs -pvs"]/div/div/span/text()')
        yield loader.load_item()
        
       

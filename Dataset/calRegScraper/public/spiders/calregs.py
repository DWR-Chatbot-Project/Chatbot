from scrapy.spiders import CrawlSpider, Rule
import scrapy
from scrapy.linkextractors import LinkExtractor
from dotenv import load_dotenv
from w3lib.url import url_query_cleaner
from public.items import Regulation
import re, os, urllib.parse


load_dotenv()


def get_url(url):
    payload = {"api_key": os.getenv("SCRAPER_API"), "url": url, "country_code": "us"}
    proxy_url = 'http://api.scraperapi.com/?' + urllib.parse.urlencode(payload)
    return proxy_url

class RuleSpider(CrawlSpider):
    name = 'calregs'
    allowed_domains = ['govt.westlaw.com']
    # start_urls = [
    #     'https://govt.westlaw.com/calregs/Index?transitionType=Default&contextData=%28sc.Default%29',
    #     'https://govt.westlaw.com/calregs/Browse/Home/California/CaliforniaCodeofRegulations?guid=I717E98405B6111EC9451000D3A7C4BC3&originationContext=documenttoc&transitionType=Default&contextData=(sc.Default)']
    
    rules = (
        Rule(LinkExtractor(
            deny=[
                re.escape('https://govt.westlaw.com/offsite'),
                re.escape('https://govt.westlaw.com/whitelist-offsite'),
                re.escape('https://next.westlaw.com'),
            ],
        ), 
        process_links='process_links',
        callback='parse_page', 
        follow=True),
    )
    
    def process_links(self, links):
        for link in links:
            link.url = url_query_cleaner(link.url)
            yield link
    
    def start_requests(self):
        start_url = "https://govt.westlaw.com/calregs/Browse/Home/California/CaliforniaCodeofRegulations?guid=I717E98405B6111EC9451000D3A7C4BC3&originationContext=documenttoc&transitionType=Default&contextData=(sc.Default)"
        yield scrapy.Request(url=start_url, callback=self.parse_response)
    
    def parse_response(self, response):
        item = Regulation()
        # links = response.xpath("//*[@id='co_contentColumn']")
        links = response.xpath("//ul[@class='co_genericWhiteBox']/li/a/@href")
        
        for link in links:
            url = link.get()
            page_url = f"https://govt.westlaw.com/{url}"
            
            yield scrapy.Request(page_url, callback=self.parse_chapter, meta={"item": item})
        
    def parse_chapter(self, response):
        item = response.meta["item"]
        item["chapter"] = response.xpath("//h1/text()").get()
        
        links = response.xpath("//ul[@class='co_genericWhiteBox']/li/a/@href")
        
        for link in links:
            url = link.get()
            page_url = f"https://govt.westlaw.com/{url}"
            
            yield scrapy.Request(page_url, callback=self.parse_article, meta={"item": item})
            
    def parse_article(self, response):
        item = response.meta["item"]
        item["article"] = response.xpath("//h1/text()").get()
        
        links = response.xpath("//ul[@class='co_genericWhiteBox']/li/a/@href")
        
        for link in links:
            url = link.get()
            page_url = f"https://govt.westlaw.com/{url}"
            
            yield scrapy.Request(page_url, callback=self.parse_page, meta={"item": item})
    
    def parse_page(self, response):
        # item['rule_url'] = response.url
        item = response.meta["item"]
        item["title"] = response.xpath("//div[@class='co_title']/div/strong/text()").get()
        
        str = ""
        for block in response.css("div.co_contentBlock.co_body"):
            text = block.xpath('.//text()').getall()
            str = str.join(text)
            
        item['paragraphText'] = str
        return item
        
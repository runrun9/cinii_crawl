# -*- coding: utf-8 -*-
import scrapy
import urllib
from cinii_crawl.items import CiniiCrawlItem


class RunSpider(scrapy.Spider):
    name = 'run'
    allowed_domains = ['ci.nii.ac.jp']
    # query = urllib.parse.quote_plus("自然言語処理", encoding="utf-8")
    start_urls = ["https://ci.nii.ac.jp/search?q=自然言語処理&range=2&count=20&sortorder=1&type=0"]
    count = 0
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 360,
    }

    def parse(self, response):
        self.count += 1
        if self.count > 200:
            return

        for paper in response.css("dl.paper_class"):
            url = "https://"+self.allowed_domains[0]+paper.css("dt > a::attr('href')").extract_first()
            abstract = paper.css("dd > p.item_snipet.item_summry.description::text").extract_first().replace("\n", "").replace("\t", "")
            if abstract:
                yield scrapy.Request(url, callback=self.paper_parse)

        next_page = "https://"+self.allowed_domains[0]+response.css("#resultlist > div.paging > ul a[rel='next']::attr('href')").extract_first()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

    def paper_parse(self, response):
        if response.css("#nav-content > ul.nav.navbar-nav.menu-utility-list > li:nth-child(3) > a::text").extract_first() == "Japanese":
            url = "https://"+self.allowed_domains[0]+response.css("#nav-content > ul.nav.navbar-nav.menu-utility-list > li:nth-child(3) > a::attr('href')").extract_first()
            yield scrapy.Request(url, callback=self.paper_parse)
            return

        item = CiniiCrawlItem()
        item["url"] = response.url
        item["title"] = response.css("#paperdata > h1 > span::text").extract_first().replace("\n", "").replace("\t", "")
        item["abstract"] = response.css("#itemdatatext > div:nth-child(5) > div > p.abstracttextjpn.entry-content::text").extract_first()
        item["keyphrase"] = response.css("#keyword > ul > li > a::text").extract()
        #itemdatatext > div:nth-child(5) > div > p.abstracttextjpn.entry-content
        if item["abstract"] and item["keyphrase"]:
            yield item

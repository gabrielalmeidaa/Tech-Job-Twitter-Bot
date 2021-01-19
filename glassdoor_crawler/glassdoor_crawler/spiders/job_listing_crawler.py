import re

import scrapy
from scrapy.spiders import CrawlSpider


class JobListingSpider(CrawlSpider):
    name = 'job_listing'
    mongo_collection = 'glassdoor'
    duplicity_condition = ['title', 'url']

    def __init__(self, delta='1988-01-01'):
        super(JobListingSpider, self).__init__()
        self.delta = delta
        self.BASE_URL = "https://www.glassdoor.com.br"
        self.LISTING_URL = "https://www.glassdoor.com.br/Vaga/" \
                           "bras%C3%ADlia-vagas-SRCH_IL.0,8_IC2494161.htm?radius=62&industryId=1063"

    def start_requests(self):
        yield scrapy.Request(url=self.LISTING_URL, method="GET", callback=self.parse_pages)

    def parse_pages(self, response):
        page_limit = self.get_page_limit(response)

        for page in range(0, int(page_limit) + 1):
            url = self.LISTING_URL + "&p={}".format(str(page))
            yield scrapy.Request(url=url, method="GET", callback=self.parse_job_listings)   # FIXME: Page changes is broken. Using Selenium is probably the solution.

    def parse_job_listings(self, response):
        for job in response.xpath('//article[@id="MainCol"]/div[1]/ul'):
            title = job.xpath('div[2]/a[1]//text()').extract_first()
            url = self.BASE_URL + job.xpath('div[2]/a[1]/@href').extract_first()
            job_age = job.xpath('descendant::div[@data-test="job-age"]/text()').extract_first()
            yield dict(title=title, url=url, job_age=job_age)

    @staticmethod
    def get_page_limit(response):
        page_limit_text = response.xpath('//div[@data-test="page-x-of-y"]/text()').extract_first()
        pages = re.compile('[0-9]+').findall(page_limit_text)
        return pages[-1]


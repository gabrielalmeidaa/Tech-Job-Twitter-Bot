import scrapy
from scrapy.spiders import CrawlSpider


class JobListingSpider(CrawlSpider):
    def parse(self, response, **kwargs):
        pass

    name = 'job_listing'
    mongo_collection = 'glassdoor'
    duplicity_condition = ['id']

    def __init__(self, delta='1988-01-01'):
        super(JobListingSpider, self).__init__()
        self.delta = delta

    def start_requests(self):
        LISTING_URL = "https://www.glassdoor.com.br/Vaga/bras%C3%ADlia-vagas-SRCH_IL.0,8_IC2494161.htm?radius=62&industryId=1063"
        yield scrapy.Request(url=LISTING_URL, method="GET", callback=self.get_job_items)

    def get_job_items(self, response):
        import pdb; pdb.set_trace()

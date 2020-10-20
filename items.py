import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    salary = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    currency = scrapy.Field()
    _id = scrapy.Field()
    vacancy_link = scrapy.Field()
    #site_scraping = scrapy.Field()
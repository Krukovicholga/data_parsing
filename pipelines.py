# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter

from pymongo import MongoClient


class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy140920_99

    def process_item(self, item, spider):

        salary = item['salary']
        if spider.name == "hhru":
            item['vacancy_link'] = item['vacancy_link'][0]
            for i in range(len(salary)):
                salary[i] = salary[i].replace(u'\xa0', u'')
            if salary[0] == 'до ':
                item['max_salary'] = salary[1]
                item['min_salary'] = 'не указана'
                item['currency'] = salary[-2]
            elif salary[0] == 'от ' and len(salary) <= 5:
                item['min_salary'] = salary[1]
                item['max_salary'] = 'не указана'
                item['currency'] = salary[-2]
            elif len(salary) > 5:
                item['min_salary'] = salary[1]
                item['max_salary'] = salary[3]
                item['currency'] = salary[-2]
            elif len(salary) == 1:
                item['min_salary'] = 'не указана'
                item['max_salary'] = 'не указана'
                item['currency'] = 'не указана'

        if spider.name == "superjob":
            if salary[0] == 'до':
                item['max_salary'] = salary[2].split('\xa0')[0] + salary[2].split('\xa0')[1]
                item['min_salary'] = 'Не указана'
                item['currency'] = salary[2].split('\xa0')[2]
            elif salary[0] == 'от':
                item['min_salary'] = salary[2].split('\xa0')[0] + salary[2].split('\xa0')[1]
                item['max_salary'] = 'Не указана'
                item['currency'] = salary[2].split('\xa0')[2]
            elif len(salary) == 4:
                item['max_salary'] = salary[0].replace("\xa0", "")
                item['min_salary'] = salary[1].replace("\xa0", "")
                item['currency'] = salary[3].replace("\xa0", "")
            elif len(salary) == 1:
                item['max_salary'] = salary[0]
                item['min_salary'] = salary[0]
                item['currency'] = 'Не указана'
            else:
                item['max_salary'] = salary[0]
                item['min_salary'] = salary[0]
                item['currency'] = salary[2]

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item

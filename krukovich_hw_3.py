from pymongo import MongoClient
from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re


client = MongoClient('127.0.0.1', 27017)
db = client['hh_db']
vacancies = db.vacancies
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/84.0.4147.135 Safari/537.36'}
jobs=[]


def hh():
    i = 0
    jobs = []
    while True:
        html = f'https://spb.hh.ru/search/vacancy?L_is_autosearch=false&area=2&clusters=true&enable_snippets=true&page={i}'
        soup = bs(requests.get(html, headers=headers).text, 'html.parser')
        jobs_block = soup.find('div', {'class': 'vacancy-serp'})
        jobs_list = jobs_block.findChildren(recursive=False)
        for job in jobs_list:
            job_data = {}
            new_list = job.find('span', {'class': 'g-user-content'})
            if new_list != None:
                main_info = new_list.findChild()
                job_name = main_info.getText()
                job_link = main_info['href']
                vacancy_id = job_link.split('/')
                vacancy_id = vacancy_id[4]
                salary = job.find('div', {'class': 'vacancy-serp-item__sidebar'})
                salary = salary.getText()
                salary = salary.replace(u'\xa0', u'')
                salaries = salary.split('-')
                salaries[0] = re.sub(r'[^0-9]', '', salaries[0])
                salary_min = salaries[0]
                if salaries[0] == '':
                    salary_min = None
                if len(salaries) > 1:
                    salaries[1] = re.sub(r'[^0-9]', '', salaries[1])
                    salary_max = int(salaries[1])
                else:
                    salary_max = None
                job_data['vacancy'] = job_name
                job_data['salary_min'] = salary_min
                job_data['salary_max'] = salary_max
                job_data['link'] = job_link
                job_data['vacancy_id']=vacancy_id
                jobs.append(job_data)
                duplicates = vacancies.find_one({'vacancy_id': vacancy_id})
                if duplicates == None:
                    vacancies.insert_one(job_data)
                else:
                    continue
        i += 1
        if not soup.find('a', attrs={'data-qa':'pager-next'}):
            break


def find_salary(salary):
    salaries = vacancies.find({'$or':[{'salary_min': {'$gt': salary}}, {'salary_max': {'$gt': salary}}]})
    for sum in salaries:
        pprint(sum)


hh()
salary = int(input('Введите размер зарплаты: '))
find_salary(salary)
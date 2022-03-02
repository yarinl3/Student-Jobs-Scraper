"""
Scraping student jobs (for me) from https://www.jobmaster.co.il.
"""
__version__ = '1.0.0'
__author__ = 'Yarin Levi <yarinl330@gmail.com>'

from bs4 import BeautifulSoup
import requests


def jobmaster():
    page = 1
    jobs = []
    while True:
        url = f'https://www.jobmaster.co.il/jobs/?currPage={page}&q=סטודנטים+למחשבים'
        req = requests.get(url).content.decode('utf-8')
        page += 1
        if 'לא נמצאו תוצאות' in req:
            break

        soup = BeautifulSoup(req, 'html.parser')
        articles = soup.find_all('article', {'class': 'CardStyle JobItem font14'})
        for article in articles:
            links = article.find_all('a')
            link = links[0]['href']
            if 'jobs' in link:
                job_link = f'https://www.jobmaster.co.il{link}'
            else:
                job_link = ''
            job_title = article.find('div', {'class': 'CardHeader'}).text
            jobs.append(f"{job_link}|||{job_title.replace('|||', ' ')}")

    with open('Jobs files/JobMaster.txt', 'w', encoding='utf-8') as fd:
        for job in jobs:
            fd.write(f'{job}\n')

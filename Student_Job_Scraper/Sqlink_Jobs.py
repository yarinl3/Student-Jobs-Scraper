"""
Scraping student jobs (for me) from https://www.sqlink.com.
"""
__version__ = '1.0.0'
__author__ = 'Yarin Levi <yarinl330@gmail.com>'

from bs4 import BeautifulSoup
import requests


def sqlink():
    page = 1
    jobs = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"}
    while True:
        url = f'https://sqlink.com/career/student/בוגרי-תוכנה/?page={page}'
        req = requests.get(url, headers=headers, verify=False).content.decode('utf-8')
        page += 1
        soup = BeautifulSoup(req, 'html.parser')
        job_divs = soup.find_all('div', {'class': 'col10'})
        for job_div in job_divs:
            links = job_div.find_all('a')
            job_link = ''
            job_title = ''
            for link in links:
                if '/career/student/' in link['href']:
                    job_link = link['href']
                    job_title = link.text.replace('\n', '')
            jobs.append(f"{job_link}|||{job_title.replace('|||', ' ')}")
        if f'page={page}' not in req:
            break

    with open('Jobs files/Sqlink.txt', 'w', encoding='utf-8') as fd:
        for job in jobs:
            fd.write(f'{job}\n')
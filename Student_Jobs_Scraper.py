"""
Scraping student jobs (for me) from https://t.me/HiTech_Jobs_In_Israel.
"""
__version__ = '1.0.1'
__author__ = 'Yarin Levi <yarinl330@gmail.com>'

import json
from prettytable import PrettyTable


def main():
    blocked_job_titles = [i.replace('\n', '') for i in
                          open('Jobs files/blocked_job_titles.txt', encoding='utf-8').readlines()]
    blocked_job_locations = [i.replace('\n', '') for i in
                             open('Jobs files/blocked_job_location.txt', encoding='utf-8').readlines()]
    unfiltered_jobs = make_list()
    filtered_jobs, filtered_hebrew_jobs = make_filtered_job_list(unfiltered_jobs, blocked_job_titles, blocked_job_locations)
    # print(make_pretty(filtered_jobs))
    # print(make_pretty(filtered_hebrew_jobs, hebrew=True))
    all_jobs = filtered_jobs + filtered_hebrew_jobs
    while True:
        pop_job = all_jobs.pop()
        link = pop_job[2]
        while check_exist_in_expired(link) is True or check_exist_in_sent(link) is True or already_sent(link) is True:
            pop_job = all_jobs.pop()
            link = pop_job[2]
        print(f'\nTotal jobs: {len(all_jobs)}')
        print(pop_job)
        choose = input('press 1 if expired, 3 if the resume sent, any other keys to do nothing.\n')
        if choose == '1':
            check_exist_in_expired(link, add=True)
        elif choose == '3':
            check_exist_in_sent(link, add=True)
        else:
            all_jobs.append(pop_job)


def already_sent(link):
    companies = [i.replace('\n', '') for i in open('Jobs files/companies.txt', encoding='utf-8').readlines()]
    if True in [(i.lower() in link.lower()) for i in companies]:
        return True
    return False


def check_exist_in_expired(url, add=False):
    with open('Jobs files/expired.txt', encoding='utf-8', mode='a+') as fd:
        if add is False:
            fd.seek(0)
        if f'{url}\n' in fd.readlines():
            return True
        if add is True:
            fd.write(f'{url}\n')
    return False


def check_exist_in_sent(url, add=False):
    with open('Jobs files/Sent.txt', encoding='utf-8', mode='a+') as fd:
        if add is False:
            fd.seek(0)
        if f'{url}\n' in fd.readlines():
            return True
        if add is True:
            fd.write(f'{url}\n')
    return False


# Creates a list that contains all jobs for students:
def make_list():
    jobs = []
    site_json = json.loads(open('Jobs files/result.json', encoding='utf-8').read())
    for i in site_json['messages']:
        for j in i['text']:
            try:
                if type(j) == dict and 'student' in j['text'].lower():
                    jobs.append(i['text'])
                    break
            except KeyError:
                pass
    return jobs


def make_pretty(jobs, hebrew=False):
    table = PrettyTable()
    if hebrew is True:
        table.field_names = ['משרה', 'מיקום', 'קישור']
    else:
        table.field_names = ["Job title", "Location", "Link"]
    for i in jobs:
        table.add_row(i)
    return table


def make_filtered_job_list(jobs, blocked_job_titles, blocked_job_locations):
    """Filter jobs by keywords and locations"""
    filtered_jobs = []
    filtered_hebrew_jobs = []
    for job in jobs:
        try:
            job_title = job[0]['text'].replace('\n', '')
            job_location = job[1].replace('\n', '')
            job_link = job[2]['href'].replace('\n', '')
            block_flag = False

            # Cuts the location from the sentence:
            if job_location.find('Location:') != -1 and job_location.find('Press') != -1:
                job_location = job_location[job_location.find('Location:')+10:job_location.find('Press')]

            for title in blocked_job_titles:
                if title.lower() in job_title.lower() and 'software' not in job_title.lower():
                    block_flag = True
                    break

            if block_flag is False:
                for location in blocked_job_locations:
                    # Leaves in the list jobs with several locations including Tel Aviv:
                    if location.lower() in job_location.lower() and 'tel ' not in job_location.lower()\
                            and 'tel-' not in job_location.lower():
                        block_flag = True
                        break

            if block_flag is False:
                if True in [ord('א') <= ord(i) <= ord('ת') for i in job_title]:
                    filtered_hebrew_jobs.append([job_title, job_location, job_link])
                else:
                    filtered_jobs.append([job_title, job_location, job_link])

        except TypeError:
            pass
        except KeyError:
            pass
    return filtered_jobs, filtered_hebrew_jobs


if __name__ == '__main__':
    try:
        main()
    except IndexError:
        print('You checked the whole list :)')

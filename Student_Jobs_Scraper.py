"""
Scraping student jobs (for me) from https://t.me/HiTech_Jobs_In_Israel.
"""
__version__ = '1.0.0'
__author__ = 'Yarin Levi <yarinl330@gmail.com>'

import json
from prettytable import PrettyTable

site_json = json.loads(open('result.json', encoding='utf-8').read())
jobs = []
jobs_counter = 0
tb = PrettyTable()
tb.field_names = ["Job title", "Location", "Link"]
hebrew_tb = PrettyTable()
hebrew_tb.field_names = ['משרה', 'מיקום', 'קישור']

# Creates a list that contains all jobs for students:
for i in site_json['messages']:
    for j in i['text']:
        try:
            if type(j) == dict and 'student' in j['text'].lower():
                jobs.append(i['text'])
                break
        except KeyError:
            pass

# Unwanted keywords:
blocked_job_titles = ['Senior', 'Receptionist', 'Design', 'Support', 'Account', 'Mechanic', 'Engineer', 'Law',
                      'Technic', 'Sale', 'Hardware', 'HW ', 'Chip', 'Customer', 'HR ', 'Admin', 'Business',
                      'Talent', 'IT ', 'IT/', 'Electronic', 'PMO ', 'Manage', 'Benefit', 'Campaign', 'PhD', 'Service',
                      'Financ', 'Recruiter', 'Signal', 'Optic', 'Physical', 'Coordinator', 'Chemistry', 'Market']

# Unwanted locations:
blocked_job_locations = ['Haifa', 'Jerusalem', "Yokne'am", "Yokne’am", 'Yokneam', 'Beer Sheva', 'Beer-Sheva', 'Migdal',
                         'Caesarea', 'Netanya', 'Ashkelon', 'Kfar Netter', "Yizre'el", ]

# Filter jobs by keywords and locations:
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
            jobs_counter += 1
            if True in [ord('א') <= ord(i) <= ord('ת') for i in job_title]:
                hebrew_tb.add_row([job_title, job_location, job_link])
            else:
                tb.add_row([job_title, job_location, job_link])
    except TypeError:
        pass
    except KeyError:
        pass
print(tb)
print(hebrew_tb)
print(f'\nTotal jobs: {jobs_counter}')

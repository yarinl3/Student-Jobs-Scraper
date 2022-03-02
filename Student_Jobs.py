from Student_Job_Scraper import *
import time
wishlist_copy = None


def main():
    clear()
    print('Hello student :)\n'
          'What do you want to do? (choose a number)\n')
    while True:
        choice = input('1. Scrap from sites\n'
                       '2. Show jobs that scraped\n'
                       '3. Pop scrapped jobs\n'
                       '4. Pop wishlist jobs\n'
                       '5. Exit\n')
        clear()
        if choice == '1':
            while True:
                print('What site do you want to scrap?')
                site = input('1. AllJobs\n'
                             '2. Job Master\n'
                             '3. Drushim\n'
                             '4. SQLink\n'
                             '5. Telegram chat history\n'
                             '6. Scrap all\n')
                if site not in ['1', '2', '3', '4', '5', '6']:
                    clear()
                    print('Bad choice, please try again\n')
                    time.sleep(2)
                    clear()
                else:
                    clear()
                    scrap(site)
                    return
        elif choice == '2':
            for job in load_jobs():
                print(job[0], job[1] + u'\u202B')
            return
        elif choice == '3':
            pop_jobs()
            return
        elif choice == '4':
            pop_jobs(wishlist=True)
            return
        elif choice == '5':
            return
        else:
            print('Bad choice, please try again\n')
            time.sleep(2)
        clear()


def scrap(choice):
    names = {'1': 'AllJobs', '2': 'Job Master', '3': 'Drushim', '4': 'SQLink', '5': 'Telegram'}
    funcs = {'1': alljobs, '2': jobmaster, '3': drushim, '4': sqlink, '5': telegram_jobs}

    if choice == '6':
        for i in range(1, 6):
            jobs_scrap(names[str(i)], funcs[str(i)])
    else:
        jobs_scrap(names[choice], funcs[choice])


def jobs_scrap(name, func):
    try:
        func()
        print(f'{name} scraped successfully.')
    except Exception as e:
        print(f'{name} scraping failed.')
        if name != 'Telegram' or type(e) != Exception:
            print(f'\tError: {str(e.__class__)[8:-2]}\n')


def load_jobs():
    jobs = []
    for filename in ['Telegram', 'Sqlink', 'AllJobs', 'DrushimJobs', 'JobMaster']:
        try:
            with open(f'Jobs files/{filename}.txt', 'r', encoding='utf-8') as fd:
                for line in fd:
                    job_link, job_title = line.split('|||')
                    jobs.append([job_link, job_title.replace('\n', '')])
        except FileNotFoundError:
            pass
    return jobs


def load_wishlist():
    jobs = []
    try:
        with open(f'Jobs files/wishlist.txt', encoding='utf-8', mode='r') as fd:
            fd.seek(0)
            for line in fd:
                job_link, job_title = line.split('|||')
                jobs.append([job_link, job_title.replace('\n', '')])
    except FileNotFoundError:
        pass
    open(f'Jobs files/wishlist.txt', 'w').close()
    return jobs


def update_wishlist(jobs):
    with open('Jobs files/wishlist.txt', encoding='utf-8', mode='a+') as fd:
        wishlist_content = fd.read()
        for job in jobs:
            link = job[0]
            title = job[1]
            if link not in wishlist_content:
                fd.write(f"{link}|||{title.replace('|||', ' ')}\n")


def pop_jobs(wishlist=False):
    global wishlist_copy
    if wishlist is True:
        jobs = load_wishlist()
        wishlist_copy = jobs
    else:
        jobs = load_jobs()
    while True:
        clear()
        with open('Jobs files/unwanted_keywords.txt', encoding='utf-8', mode='r') as fd:
            keywords = fd.read().split('\n')
            while True:
                job = jobs.pop()
                if wishlist is True:
                    wishlist_copy.pop()
                link = job[0]
                title = job[1].replace('\n', '')
                if True not in [check_exist(link, i) for i in ['blacklist', 'sent', 'wishlist']] and \
                        (True not in [keyword.lower() in f'{title.lower()} {link.lower()}' for keyword in keywords] or
                         'סטודנט' in title or 'student' in title.lower()):
                    break
        print(f'Total jobs: {len(jobs) + 1}')
        print(f'\n{title}' + u'\u202B')
        print(f'{link}\n')
        choice = input('1. Add to blacklist\n'
                       '2. Save to wishlist\n'
                       '9. Add to sent\n'
                       '4. Exit\n')
        if choice == '1':
            check_exist(link, 'blacklist', add=True)
        elif choice == '2':
            check_exist(link, 'wishlist', add=True, wishlist_title=title)
        elif choice == '9':
            check_exist(link, 'sent', add=True)
        else:
            jobs.append(job)
            if wishlist is True:
                wishlist_copy.append(job)
        if choice == '4':
            if wishlist is True:
                update_wishlist(jobs)
            return
        time.sleep(0.5)


def check_exist(url, filename, add=False, wishlist_title=None):
    try:
        with open(f'Jobs files/{filename}.txt', encoding='utf-8', mode='r') as fd:
            pass
    except FileNotFoundError:
        with open(f'Jobs files/{filename}.txt', encoding='utf-8', mode='w') as fd:
            pass
    with open(f'Jobs files/{filename}.txt', encoding='utf-8', mode='a+') as fd:
        fd.seek(0)
        for line in fd:
            if f'{url}' in line:
                return True
        if add is True:
            if wishlist_title is None:
                fd.write(f'{url}\n')
            else:
                fd.write(f"{url}|||{wishlist_title.replace('|||', ' ')}\n")
    return False


def handle_errors():
    try:
        main()
    except IndexError as e:
        if str(e) == 'pop from empty list':
            print('You went through the entire list of jobs.\n'
                  'For new jobs, please try scraping again.')
    except Exception:
        if wishlist_copy is not None:
            update_wishlist(wishlist_copy)


if __name__ == '__main__':
    handle_errors()

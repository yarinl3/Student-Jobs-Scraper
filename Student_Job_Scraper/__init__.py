"""
Scraping student jobs.
"""
__version__ = '1.0.0'
__author__ = 'Yarin Levi <yarinl330@gmail.com>'

from .Job_Master import jobmaster
from .Sqlink_Jobs import sqlink
from .Drushim_Jobs import drushim
from .AllJobs_Scraper import alljobs
from .Telegram_Jobs_Scraper import telegram_jobs
import os
import warnings


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


warnings.filterwarnings("ignore")
try:
    os.mkdir('Jobs files')
except Exception:
    pass

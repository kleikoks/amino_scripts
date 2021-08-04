import datetime
import logging
import subprocess

from celery import Celery
from celery.signals import after_setup_logger
from celery.schedules import crontab
from utils import get_file_path


app = Celery('tasks', broker='pyamqp://guest@localhost//')
loggerr = logging.getLogger(__name__)

@app.task()
def sendcoin():
    tz = ((23 - datetime.datetime.utcnow().hour) * 60)
    if tz != 0:
        env_path= '/home/kleikoks/projects/amino_scripts/venv/bin/'
        loggerr.warning('SENDCOIN STARTED')
        subprocess.run(
            ['python3', '/' + get_file_path(__file__, 'sendcoins_1.py')],
            env={'PATH': env_path},
            check=False,
            timeout=None
        )
        loggerr.warning('SENDCOIN ENDED')
        loggerr.warning('COIN STARTED')
        subprocess.run(
            ['python3',  '/' + get_file_path(__file__, 'coin.py')],
            env={'PATH': env_path},
            check=False,
            timeout=None
        )
        loggerr.warning('COIN ENDED')

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='20', hour='*'), sendcoin.s())

@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter('%(asctime)s %(name)-16s %(funcName)-12s %(message)s')
    fh = logging.FileHandler('logs/tasks.log')
    fh.setFormatter(formatter)
    fh.setLevel('WARNING')
    logger.addHandler(fh)

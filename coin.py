import json
import logging
from datetime import datetime
from time import time

from concurrent.futures import ProcessPoolExecutor

from amino import Client
from amino import SubClient
from amino.lib.util.exceptions import (
    InvalidPassword,
    InvalidAccountOrPassword,
    VerificationRequired
)


CID = "72200141"
with open('accounts.json', 'r') as f:
    dictlist = json.load(f)
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(name)-16s %(funcName)-12s %(filename)-12s %(message)s')
fh = logging.FileHandler('logs/coin.log')
fh.setFormatter(formatter)
fh.setLevel('WARNING')
logger.addHandler(fh)
timezone = (23 - datetime.utcnow().hour) * 60
def timer():
    toime = {"start": int(datetime.timestamp(datetime.now())), "end": int(
        datetime.timestamp(datetime.now()))+300}
    return toime

def sendobj(sub: SubClient):
    timers = [
        timer(), timer(), timer(), timer(), timer(), timer(
        ), timer(), timer(), timer(), timer(), timer(), timer()
    ]
    sub.send_active_obj(timers=timers, tz=timezone, timestamp=int(time() * 1000))

def log(cli: Client, email: str, password: str):
    try:
        cli.login(email=email, password=password)
    except Exception as e:
        logger.warning("Log %s: %s %s", email, password, e)

def task(sub: SubClient, email: str, i: int):
    try:
        sendobj(sub)
    except Exception as e:
        logger.critical('Task Exception %s', e)

def threadit(email: str, device: str, password: str):
    client = Client(deviceId=device)
    log(cli=client, email=email, password=password)
    client.join_community(CID)
    subclient = SubClient(comId=CID, profile=client.profile)
    with ProcessPoolExecutor(max_workers=25) as executor:
        _ = [executor.submit(task, subclient, email, i) for i in range(25)]
    client.logout()

def main():
    logger.critical("%s всего аккаунтов", len(dictlist))
    with ProcessPoolExecutor(max_workers=7) as executor:
        executed_tasks = [executor.submit(
            threadit, i, dictlist[i]['device'], dictlist[i]['password']
            ) for i in dictlist]
    logger.critical("Готово. %s", len(executed_tasks))

if __name__ == '__main__':
    main()

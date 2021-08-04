import json
import logging
import random

from multiprocessing import Manager
from concurrent.futures import ProcessPoolExecutor

from amino import Client
from amino import SubClient
from amino.lib.util.exceptions import (
    InvalidPassword,
    InvalidAccountOrPassword,
    VerificationRequired
)


CID = '11383715'
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(name)-16s %(funcName)-12s %(filename)-12s %(message)s')
fh = logging.FileHandler('logs/sendcoins_1.log')
fh.setFormatter(formatter)
fh.setLevel('WARNING')
logger.addHandler(fh)
blog = random.choice([
    "http://aminoapps.com/p/1jein2",
    "http://aminoapps.com/p/4va49k",
    "http://aminoapps.com/p/mu5j4p"
])
with open('accounts.json', 'r') as f:
    dictlist = json.load(f)

def log(cli: Client, email: str, password: str):
    try:
        cli.login(email=email, password=password)
    except VerificationRequired:
        logger.warning("%s: Требует подтверждения.", email)
    except (InvalidPassword, InvalidAccountOrPassword):
        logger.warning("InvalidPassword InvalidAccountOrPassword %s", email)
    except Exception as e:
        logger.warning("%s: %s", email, e)

def threadit(email: str, device: str, password: str, result_value):
    client = Client(deviceId=device)
    log(cli=client, email=email, password=password)
    client.join_community(CID)
    subclient = SubClient(comId=CID, profile=client.profile)
    try:
        subclient.lottery()
    except:
        pass
    coins = int(client.get_wallet_info().totalCoins)
    result_value.value += min(coins, 500)
    blogx = client.get_from_code(blog).objectId
    if coins > 0:
        subclient.send_coins(blogId=blogx, coins=min(coins, 500))
        coins -= min(coins, 500)
    client.logout()
    return 1

def main():
    result_value = Manager().Value('i', 0)
    logger.warning("%s аккаунтов загружено.", len(dictlist))
    with ProcessPoolExecutor(max_workers=50) as executor:
        _ = [executor.submit(
            threadit, i, dictlist[i]['device'], dictlist[i]['password'], result_value
        ) for i in dictlist]
    logger.warning("Всього монеток %s в безодню дупу цього чоловіка %s", result_value.value, blog)

if __name__ == '__main__':
    main()

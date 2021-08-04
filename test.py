from datetime import datetime
import json
import logging
import time
import random

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(name)-16s %(funcName)-12s %(filename)-12s %(message)-5s')
formatter.converter = time.localtime
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)
logging.Formatter.converter = time.gmtime
# logger.critical(int(datetime.timestamp(datetime.now())))
with open('accounts.json', 'r') as f:
    dictlist = json.load(f)

logger.warning("%{}s аккаунтов загружено.", len(dictlist))

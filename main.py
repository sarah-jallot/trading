import krakenex
import json
import time
import datetime
import calendar
from utils import *


if __name__ == '__main__':
    api = krakenex.API()
    api.load_key('kraken.key')
    pair = ('XETH','ZUSD') #cryptocurrency name versus USD
    since = str(int(time.time() - 3600))
   # print(json.dumps(get_fake_trades_history(), indent=4))  # timestamp from one hour ago
    analyze(pair, since)



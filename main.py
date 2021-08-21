import krakenex
import time
from trading.utils import *
from trading.investing_strategies import analyze


if __name__ == '__main__':
    api = krakenex.API()
    api.load_key('kraken.key')
    pair = ('XETH','ZUSD') #cryptocurrency name versus USD
    since = str(int(time.time() - 3600))
   # print(json.dumps(get_fake_trades_history(), indent=4))  # timestamp from one hour ago
    analyze(api, pair, since)



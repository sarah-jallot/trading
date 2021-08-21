import krakenex
import time
import json
from utils import get_fake_trades_history, get_crypto_data
from investing_strategies import simple_analyze



if __name__ == '__main__':
    api = krakenex.API()
    api.load_key('kraken.key')
    pair = ('XETH','ZUSD') #cryptocurrency name versus EUR
    since = str(int(time.time() - 3600))
    simple_analyze(pair, since, api)
    #print(json.dumps(get_crypto_data(pair[0]+pair[1], since, api), indent=4))
    #print(len(get_crypto_data(pair[0]+pair[1], since, api)))


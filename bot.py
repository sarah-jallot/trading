import krakenex
import json
import time
import datetime
import calendar

api = krakenex.API()
api.load_key('kraken.key')

pair = 'XETHZUSD' #cryptocurrency name versus USD
since = str(int(time.time() - 3600)) # timestamp from one hour ago
api.query_public('OHLC', data = {'pair': pair, 'since': since}) # open high low close


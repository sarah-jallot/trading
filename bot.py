import krakenex
import json
import time
import datetime
import calendar
def get_crypto_data(pair, since):
    return api.query_public('OHLC', data={'pair': pair, 'since': since})["result"][pair]

def get_balance():
    return api.query_private('Balance')

def get_trades_history():
    start_date = datetime.datetime(2021, 7, 4)
    end_date = datetime.datetime.today()
    return api.query_private('TradesHistory', req(start_date, end_date, 1))["result"]["trades"]

def date_mix(str_date):
    """
    Format date properly.
    """
    return calendar.timegm(str_date.timetuple())

def req(start, end, ofs):
    """
    Format request for API.
    """
    req_data = {
        'type': 'all',
        'trades': 'true',
        'start': str(date_mix(start)),
        'end': str(date_mix(end)),
        'ofs': str(ofs)
    }
    return req_data



if __name__ == '__main__':
    api = krakenex.API()
    api.load_key('kraken.key')
    pair = 'XETHZUSD' #cryptocurrency name versus USD
    since = str(int(time.time() - 3600))
    print(json.dumps(get_trades_history(), indent=4))  # timestamp from one hour ago



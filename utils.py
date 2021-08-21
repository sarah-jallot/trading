import json
import datetime
import calendar

def get_crypto_data(pair, since, api):
    return api.query_public('OHLC', data={'pair': pair, 'since': since})["result"][pair]

def get_balance(api):
    return api.query_private('Balance')

def get_fake_balance(api):
    with open('fake_data/balance.json', 'r') as f:
        return json.load(f)

def get_last_trade(pair, api):
    trades_history = get_fake_trades_history(api)['result']['trades']
    last_trade = {}
    for trade in trades_history:
        trade = trades_history[trade]
        if trade['pair'] == pair and trade['type'] == 'buy':
            last_trade = trade
    return last_trade

def get_trades_history(api):
    start_date = datetime.datetime(2021, 7, 4)
    end_date = datetime.datetime.today()
    return api.query_private('TradesHistory', req(start_date, end_date, 1))

def get_fake_trades_history(api):
    with open('fake_data/tradeshistory.json', 'r') as f:
        return json.load(f)

def date_nix(str_date):
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
        'start': str(date_nix(start)),
        'end': str(date_nix(end)),
        'ofs': str(ofs)
    }
    return req_data


def fake_update_balance(pair, dollar_amount, close_, was_sold, api):
    balance = get_fake_balance(api)
    prev_balance = float(balance['USD.HOLD'])

    new_balance = 0
    if was_sold:
        new_balance = prev_balance + float(dollar_amount)
        del balance[pair[0]]
    else:
        new_balance = prev_balance - float(dollar_amount)
        balance[pair[0]] = str(float(dollar_amount)/close_)
    balance['USD.HOLD'] = str(new_balance)

    with open('fake_data/balance.json', 'w') as f:
        json.dump(balance, f, indent=4)


def fake_buy(pair, dollar_amount, close_, last_trade, api):
    trades_history = get_fake_trades_history(api)
    last_trade['price'] = str(close_)
    last_trade['type'] = 'buy'
    last_trade['cost'] = dollar_amount
    last_trade['time'] = datetime.datetime.now().timestamp()
    last_trade['vol'] = str(float(dollar_amount/close_))

    trades_history['result']['trades'][str(datetime.datetime.now().timestamp())] = last_trade
    with open('fake_data/tradeshistory.json', 'w') as f:
        json.dump(trades_history, f, indent=4)
        fake_update_balance(pair, dollar_amount, close_, False, api)
    # api.query_private

def fake_sell(pair, dollar_amount, close_, last_trade, api):
    trades_history = get_fake_trades_history(api)
    last_trade['price'] = str(close_)
    last_trade['type'] = 'sell'
    last_trade['cost'] = str(float(last_trade['vol'])*close_)
    last_trade['time'] = datetime.datetime.now().timestamp()

    trades_history['result']['trades'][str(datetime.datetime.now().timestamp())] = last_trade

    with open('fake_data/tradeshistory.json', 'w') as f:
        json.dump(trades_history, f, indent=4)
        fake_update_balance(pair, dollar_amount, close_, was_sold=True)
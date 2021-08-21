import json
import datetime
import calendar

def get_crypto_data(api, pair, since):
    return api.query_public('OHLC', data={'pair': pair, 'since': since})["result"][pair]

def analyze(api, pair, since):
    data = get_crypto_data(api, pair[0]+pair[1], since)
    lowest = 0
    highest = 0
    for prices in data:
        balance = get_fake_balance()
        last_trade = get_last_trade(pair[0]+pair[1])
        last_trade_price = float(last_trade["price"])
        open_ = float(prices[1])
        high_ = float(prices[2])
        low_ = float(prices[3])
        close_ = float(prices[4])
        did_sell = False
        try:
            balance[pair[0]]
            selling_point_win = last_trade_price*1.005
            selling_point_loss = last_trade_price*0.995
            if open_ >= selling_point_win or close_ >= selling_point_win:
                # sell at a profit
                did_sell = True
                fake_sell(pair)
            elif open <= selling_point_loss or close_ <= selling_point_loss:
                # sell at a loss
                did_sell = True
                fake_sell(pair)
        except:
            pass

        # Logic for if we should buy
        if not did_sell and float(balance['USD.HOLD']) > 0:
            if low_ <= lowest or lowest == 0:
                lowest = low_
            if high_ >= highest:
                highest == high_

            price_to_buy = 1.0005
            if highest / lowest >= price_to_buy and low_ <= lowest:
                available_money = balance['USD.HOLD']
                # buy
                fake_buy(pair)

def fake_sell(pair, dollar_amount, close_, last_trade):
    trades_history = get_fake_trades_history()
    last_trade['price'] = str(close_)
    last_trade['type'] = 'sell'
    last_trade['cost'] = str(float(last_trade['vol'])*close_)
    last_trade['time'] = datetime.datetime.now().timestamp()

    trades_history['result']['trades'][str(datetime.datetime.now().timestamp())] = last_trade

    with open('tradeshistory.json', 'w') as f:
        json.dump(trades_history, f, indent=4)
        fake_update_balance(pair, dollar_amount, close_, was_sold=True)


def fake_update_balance(pair, dollar_amount, close_, was_sold):
    balance = get_fake_balance()
    prev_balance = float(balance['USD.HOLD'])

    new_balance = 0
    if was_sold == False:
        new_balance = prev_balance + float(dollar_amount)
        del balance[pair[0]]
    else:
        new_balance = prev_balance - float(dollar_amount)
        balance[pair[0]] = str(float(dollar_amount)/close_)
    balance['USD.HOLD'] = str(new_balance)

    with open('balance.json','w') as f:
        json.dump(balance, f, indent=4)


def fake_buy(pair, dollar_amount, close_, last_trade):
    trades_history = get_fake_trades_history()
    last_trade['price'] = str(close_)
    last_trade['type'] = 'buy'
    last_trade['cost'] = dollar_amount
    last_trade['time'] = datetime.datetime.now().timestamp()
    last_trade['vol'] = str(float(dollar_amount/close_))

    trades_history['result']['trades'][str(datetime.datetime.now().timestamp())] = last_trade
    with open('tradeshistory.json', 'w') as f:
        json.dump(trades_history, f, indent=4)
        fake_update_balance(pair, dollar_amount, close_, was_sold=False)
    # api.query_private
    pass


def get_balance(api):
    return api.query_private('Balance')

def get_last_trade(pair):
    trades_history = get_fake_trades_history()['result']['trades']
    last_trade = {}
    for trade in trades_history:
        trade = trades_history[trade]
        if trade['pair'] == pair and trade['type'] == 'buy':
            last_trade = trade
    return last_trade

def get_fake_balance():
    with open('balance.json', 'r') as f:
        return json.load(f)

def get_trades_history(api):
    start_date = datetime.datetime(2021, 7, 4)
    end_date = datetime.datetime.today()
    return api.query_private('TradesHistory', req(start_date, end_date, 1))["result"]["trades"]

def get_fake_trades_history():
    with open('tradeshistory.json','r') as f:
        return json.load(f)

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


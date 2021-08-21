from trading.utils import *

def analyze(api, pair, since):
    """
    Basic investing strategy.
    """
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
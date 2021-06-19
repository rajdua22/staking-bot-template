'''
Aloe Capital LLC
06-12-2021
MIT License
'''

from staking_bot_template.predictors.predictor import Predictor

from staking_bot_template.contracts import Proposal
from staking_bot_template.contracts import Bounds

import yfinance as yf
import numpy as np
import pandas as pd


class DumbBot(Predictor):
    def __init__(self, ticker ='ETH-USD', period = '24h', interval = '1h', starting_stake = 1):
        # Your Predictor class is allowed to be stateful
        self._ticker = ticker
        self._period = period
        self._interval = interval
        self._starting_stake = starting_stake
        
        self._upper_bound = 0
        self._lower_bound = 0
        self._stake = 0

    def periodic(self):
        super().periodic()
        data = yf.download(tickers=self._ticker, period = self._period, interval = self._interval)
        
        data_temp = data.iloc[:-2]
        increase_prices = (data_temp['High'] - data_temp['Low']) / data_temp['Open']
        mn = increase_prices.mean()
        std = increase_prices.std()
        up = mn + 2 * std

        curr_price = data.iloc[-1]['Open']

        uprange = curr_price * (1 + up)
        downrange = curr_price * (1 - up)
        
        curr_range = uprange - downrange
        last_range = data.iloc[-2]['High'] - data.iloc[-2]['Low']
        p = 1 - (last_range / curr_range)
        b = 0.5
        f = (p * (b+1) - 1) / b
        
        if f >= 0 and f <= 1:
            self._stake = self._starting_stake * f
            
        else:
            self._stake = self._starting_stake * 0.5
        
        self._upper_bound = 1 / downrange
        self._lower_bound = 1/ uprange

        print(self._lower_bound)
        print(self._upper_bound)

        self._lower_bound = np.float_(self._lower_bound).item()
        self._upper_bound = np.float_(self._upper_bound).item()
        self._stake = np.float_(self._stake).item()

        self._upper_bound = self._upper_bound * 10 ** 12 * 2 ** 48
        self._lower_bound = self._lower_bound * 10 ** 12 * 2 ** 48
        self._stake = self._stake * 10 ** 18

        
    def get_proposals(self, extra_info: dict) -> list[Proposal]:
        temp = extra_info['uniswap_bounds'].lower
        temp = float(temp)
        temp = temp / (10 ** 12 * 2 ** 48)
        print(temp)

        temp = extra_info['uniswap_bounds'].upper
        temp = float(temp)
        temp = temp / (10 ** 12 * 2 ** 48)
        print(temp)


        return [
            Proposal(
                bounds=Bounds(
                    lower=int(self._lower_bound),
                    upper=int(self._upper_bound),
                    are_inverted=False
                ),
                stake= int(self._stake)
            )
        ]

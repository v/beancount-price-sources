"""Fetch prices from World Trading Data's JSON 'api'
"""

import datetime
import json
import logging
import os
import pytz
import re
import requests

from beancount.core.number import D
from beancount.prices import source
from beancount.utils import net_utils
from datetime import datetime, date, timedelta

"""
bean-price --no-cache -e 'USD:v_sources.wtd/VTSAX'
"""

timezone = pytz.timezone('America/New_York')

class Source(source.Source):
    "World Trading Data API price extractor."

    def get_latest_price(self, ticker):
        return self.get_historical_price(ticker, date.today())

    def get_historical_price(self, ticker, date):
        """See contract in beancount.prices.source.Source."""

        date_from = date - timedelta(days=5)
        date_to = date


        url = 'https://api.worldtradingdata.com/api/v1/history' \
            '?symbol={}' \
            '&api_token={}' \
            '&date_from={}' \
            '&date_to={}'.format(
            ticker,
            os.environ['BEANCOUNT_WTD_API_TOKEN'],
            date_from,
            date_to,
        )


        logging.info("Fetching %s", url)

        r = requests.get(url)
        r.raise_for_status()

        response = r.json()

        if 'history' not in response or not response['history']:
            logging.error('No history found: response=%s', response)
            return None

        for hist_date, price_data in response['history'].items():
            # im not sure how to make this work with other currencies
            hist_date_parsed = timezone.localize(datetime.strptime(hist_date, '%Y-%m-%d'))
            return source.SourcePrice(D(price_data['close']), hist_date_parsed, 'USD')

        logging.error("Error retrieving stock info response=%s", response)
        return None


if __name__ == '__main__':
    s = Source()
    print(s.get_latest_price('VTSAX'))

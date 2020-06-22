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
from datetime import datetime, date, timedelta, timezone


"""
bean-price --no-cache -e 'USD:v_sources.wtd/VTSAX'
"""

current_tz = datetime.now(timezone.utc).astimezone().tzinfo

class Source(source.Source):
    "World Trading Data API price extractor."

    def get_latest_price(self, ticker):
        return self.get_historical_price(ticker, date.today())

    def get_historical_price(self, ticker, dt):
        """See contract in beancount.prices.source.Source."""

        if isinstance(dt, datetime):
            dt = dt.date()

        date_from = dt - timedelta(days=5)
        date_to = dt


        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}".format(
            ticker,
            os.environ['ALPHA_VANTAGE_KEY']
        )

        logging.info("Fetching %s", url)

        r = requests.get(url)
        r.raise_for_status()

        response = r.json()

        key = 'Time Series (Daily)'

        curr_date = date_to

        while curr_date > date_from:
            price_by_date = response[key]
            if str(curr_date) not in price_by_date:
                curr_date = curr_date - timedelta(days=1)
                continue
            price_data = price_by_date[str(curr_date)]
            curr_date_parsed = datetime.strptime(str(curr_date), '%Y-%m-%d').replace(tzinfo=current_tz)
            return source.SourcePrice(D(price_data['4. close']), curr_date_parsed, 'USD')

        logging.error("Error retrieving stock info response=%s", response)
        return None


if __name__ == '__main__':
    s = Source()
    print(s.get_latest_price('VTSAX'))

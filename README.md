Additional importers for beancount plaintext accounting

Installation
------------
python3 setup.py install 

World Trading Data price source
------------------------
Sign up for an API token at https://www.worldtradingdata.com

set the api token in your shell. For example, add this to your `~/.bashrc`
```
export BEANCOUNT_WTD_API_TOKEN="..."
```

Run `bean-price` commands as normal:
```
bean-price --no-cache -e 'USD:v_sources.wtd/VTSAX'
```

The ticker can be a stock symbol or mutual fund.

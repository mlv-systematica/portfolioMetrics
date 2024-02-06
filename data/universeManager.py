import pandas as pd
import numpy as np
import yfinance as yf

import requests
from requests_html import HTMLSession

class universeManager:
    
    def __init__(self) -> None:
        pass
    
    def global_market_index(self)->list:
        session = HTMLSession()
        num_currencies=250
        resp = session.get(f"https://fr.finance.yahoo.com/indices-mondiaux/?offset=0&count=250={num_currencies}")
        tables = pd.read_html(resp.html.raw_html)               
        df = tables[0].copy()
        return df.Symbole.tolist()
    
    def crypto(self)->list:
        session = HTMLSession()
        num_currencies=250
        resp = session.get(f"https://finance.yahoo.com/crypto?offset=0&count={num_currencies}")
        tables = pd.read_html(resp.html.raw_html)               
        df = tables[0].copy()
        return df.Symbol.tolist()
    
def test():
    um = universeManager()
    tickers = um.global_market_index()
    return tickers

if __name__ == "__main__":
    test()
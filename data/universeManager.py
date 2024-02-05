import pandas as pd
import numpy as np
import yfinance as yf

import requests
from requests_html import HTMLSession


class universeManager:
    
    def __init__(self) -> None:
        pass
    
    def crypto(self)->list:
        session = HTMLSession()
        num_currencies=250
        resp = session.get(f"https://finance.yahoo.com/crypto?offset=0&count={num_currencies}")
        tables = pd.read_html(resp.html.raw_html)               
        df = tables[0].copy()
        return df.Symbol.tolist()
    
def test():
    um = universeManager()
    um.crypto()

if __name__ == "__main__":
    test()
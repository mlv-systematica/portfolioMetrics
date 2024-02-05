import pandas as pd
import numpy as np
import yfinance as yf

class importManager:

    def __init__(self) -> None:
        
    def spots(tickers : list, period="5Y")->pd.DataFrame:
        if period not in ["5Y", "1Y", "1mo", "1d"]:
            raise ValueError("invalid period please use following format: 3Y, 1mo, 4d")
        
        data = pd.DataFrame()
        for ticker in tickers:
            histo = yf.Ticker(ticker).history(period="5Y")
            histo["Ticker"] = ticker
            histo.reset_index(inplace=True)
            if data.empty:
                data = histo
            else:
                data = data.append(histo)

def test():
    im = importManager()
    im.spots(["MSFT"])
    
print("ok 1")
if __name__ == "__main__":
    print("ok")
    test()
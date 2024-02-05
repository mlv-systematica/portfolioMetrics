import pandas as pd
import numpy as np
import yfinance as yf

class importManager:

    def __init__(self) -> None:
        pass
    
    def spots(self, tickers : list, period="5Y", fields = ["Open", "High", "Close", "Low", "Close", "Volume", "Dividends", "Stock Splits"])->pd.DataFrame:

        data = pd.DataFrame()
        if any([field not in ["Open", "High", "Close", "Low", "Close", "Volume", "Dividends", "Stock Splits"] for field in fields]):
            raise ValueError("Invalid input : fields not found in Histo DataFrame")
                
        for ticker in tickers:
            histo = yf.Ticker(ticker).history(period=period)[fields]
            histo["ticker"] = ticker
            if "Stock Splits" in fields: 
                histo["Stock Splits"] = histo["Stock Splits"].astype(dtype=int)
            
            if data.empty:
                data = histo
            else:
                data = data.append(histo)
        return data
        
def test():
    im = importManager()
    im.spots(["MSFT"])
    

if __name__ == "__main__":
    test()
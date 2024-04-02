import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np

from portfolio.portfolio import Portfolio
from data.importManager import importManager
import metrics

def test():
    tickers = ["XWD.TO", "^GSPC", "^STOXX50E", "^N225", "EEM", "BTC-USD", "ETH-USD", "GLD"]
    tickers_mathis = ["XWD.TO", "BTC-EUR", "ETH-EUR", "SOL-EUR", "IUIT.L","SEMI.AS", "GLD", "EEM"]
    im = importManager()
    data = im.spots(tickers_mathis)
    ptf = Portfolio(data.reset_index().drop_duplicates().pivot(index="Date", columns="ticker", values="Close"))
    
    dico_weights = {"BTC-EUR" : 477, "ETH-EUR" :234, "IUIT.L" : 154, "SEMI.AS" : 107, "SOL-EUR" : 202, "XWD.TO" : 410, "GLD" : 197, "EEM" : 50}
    weights = pd.DataFrame(index=ptf.df_price.index)
    for ticker in ptf.df_returns:
        weights[ticker] = dico_weights[ticker]
    weights=weights/sum(dico_weights.values())
    weights = np.asarray(weights.iloc[-1])
    metrics.get_vol_contribution(ptf.df_returns, weights)
    
    print("Done !")

if __name__ == "__main__":
    test()
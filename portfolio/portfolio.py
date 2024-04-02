import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np

import metrics

STRATEGY = ["EW", "MINVAR", "ERC"]

class Portfolio:
    
    def __init__(self, df_price : pd.DataFrame, start_date = "", end_date = "") -> None:
        start_date, end_date = start_date or df_price.index.min(), end_date or df_price.index.max()
        self.df_price = df_price
        self.df_returns = df_price.pct_change()
        self.start_date = start_date
        self.end_date = end_date

    def get_backtest(self,strategy : str, freq = "M", q=0.01):
        if strategy not in STRATEGY:
            raise ValueError("Strategy doesn't belongs to known strategy")
        if strategy == "EW":
            df_weights = pd.DataFrame(1/self.df_price.shape[1], index=self.df_price.index, columns=self.df_price.columns)
        
        df_returns = self.df_price.pct_change() * df_weights
        df_norm = df_returns.sum(axis=1) + 1
        df_norm.iloc[0] = 100
        df_norm = df_norm.cumprod(axis=0)
        return df_returns, df_norm       
    
    def get_quickBacktest(self, weights : pd.DataFrame, freq = "M", q = 0.01)->dict:
        ptf100 = (self.df_returns * weights).sum(axis=1)
        ptf100+=1
        ptf100.iloc[0]=100
        ptf100 = ptf100.cumprod().to_frame()
        
        df_risk_metrics = metrics.get_returns_analysis(ptf100, frequency=freq, quantile=q)
        res = {"ptf_track" : ptf100, "risk_metrics" : df_risk_metrics}
        return res
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pandas as pd
import numpy as np

import metrics

NB_DAYS_1Y = 252
NB_WEEKS_1Y = 52
NB_MONTH_1Y = 12

STANDARD_SHIFT = 0.01

FREQUENCIES = ["D", "W", "M"]
DICO_FREQ = {"D" : NB_DAYS_1Y, "W" : NB_WEEKS_1Y, "M" : NB_MONTH_1Y}

def get_returns_analysis(df_price : pd.DataFrame, frequency="D", quantile = 0.05)->tuple:
    
    if frequency not in FREQUENCIES:
        raise ValueError("Frequency not 'D', 'W' or 'M'")
    
    df_returns = df_price.resample(frequency).last().pct_change()
    df_er = df_returns.mean(axis=0) * DICO_FREQ[frequency]
    df_vol = df_returns.std(axis=0) * np.sqrt(DICO_FREQ[frequency])
    df_var, df_cvar = metrics.risk.get_var_cvar(df_price, quantile, frequency)
    df_drawdown = metrics.risk.get_drawdown(df_price)
    
    df_res = pd.DataFrame({"er" : df_er, "vol" : df_vol, "ic" : df_er/df_vol, "var" : df_var, "cvar" : df_cvar, "drawdown" : df_drawdown})
    return df_res

def get_normSpots(df_price : pd.DataFrame, start_date : str, end_date : str, tickers : list)->pd.DataFrame:
    scope = df_price.loc[start_date, end_date, tickers]
    return scope/scope.iloc[0]

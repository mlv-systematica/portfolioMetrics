import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np

NB_DAYS_1Y = 252
NB_WEEKS_1Y = 52
NB_MONTH_1Y = 12

STANDARD_SHIFT = 0.01

FREQUENCIES = ["D", "W", "M"]
DICO_FREQ = {"D" : NB_DAYS_1Y, "W" : NB_WEEKS_1Y, "M" : NB_MONTH_1Y}

def get_var_cvar(df_price : pd.DataFrame, quantile = 0.05, frequency="D"):    
    if frequency not in FREQUENCIES:
        raise ValueError("Frequency not 'D', 'W' or 'M'")
    df_returns = df_price.resample(frequency).last().pct_change()
    df_var = df_returns.quantile(q=quantile, axis=0)
    df_cvar = df_returns[df_returns <= df_var].mean(axis=0)
    return df_var, df_cvar

def get_vol(df_cov : pd.DataFrame, df_weights : pd.DataFrame)->float:
    return df_weights @ df_cov @ df_weights.T

def get_drawdown(df_price : pd.DataFrame)->float:
    return (df_price/df_price.cummax(axis=0) -1).min(axis=0)

def get_vol_contribution(df_returns : pd.DataFrame, df_weights : pd.DataFrame)->pd.DataFrame:
    risk_sensitivity, _ = get_risk_sensitivity(df_returns, df_weights)
    risk_sensitivity = (risk_sensitivity * df_weights)
    risk_sensitivity = risk_sensitivity / risk_sensitivity.sum()
    return pd.DataFrame(risk_sensitivity,index=df_returns.columns)

def get_risk_sensitivity(df_perf_rel : pd.DataFrame, weights : np.array)->tuple:
    df_cov = np.asarray(df_perf_rel.cov())
    risk_sensitivity = np.zeros(weights.shape[0])
    reference_risk_mesure = get_vol(df_cov, weights)
    for i, asset in enumerate(df_perf_rel.columns):
        if weights[i]!=0:
            bumped_weights = weights.copy()
            bumped_weights[i] *= (1+STANDARD_SHIFT)
            risk_sensitivity[i] = get_vol(df_cov, bumped_weights)
            risk_sensitivity[i] = (risk_sensitivity[i] - reference_risk_mesure) / (weights[i] * STANDARD_SHIFT)
        else:
            risk_sensitivity[i] = 0
    return risk_sensitivity, reference_risk_mesure

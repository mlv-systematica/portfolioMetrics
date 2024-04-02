import pandas as pd
import numpy as np

NB_DAYS_1Y = 252
NB_WEEKS_1Y = 52
NB_MONTH_1Y = 12

STANDARD_SHIFT = 0.01

FREQUENCIES = ["D", "W", "M"]
DICO_FREQ = {"D" : NB_DAYS_1Y, "W" : NB_WEEKS_1Y, "M" : NB_MONTH_1Y}
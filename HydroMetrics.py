# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 09:55:42 2021

@author: keyva
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from datetime import datetime
import os
import sys
import json
import math
import datetime

os.chdir("C:/Users/keyva/OneDrive/Documents/Cornell/project/IM3/CLM meeting/Metrics/")

from HydroMetrics_functions import *

# Leaf river 
LeafRiver=pd.read_csv("C:/Users/keyva/OneDrive/Documents/Cornell/project/IM3/CLM meeting/Metrics/sample_data/LeafCatch.csv")


# This scrip calculate simulated and observed and hydrologic metrics 

observed_flow=pd.read_csv("C:/Users/keyva/OneDrive/Documents/Cornell/project/IM3/CLM meeting/Metrics/sample_data/Arrow_observed.csv")
simulated_flow=pd.read_csv("C:/Users/keyva/OneDrive/Documents/Cornell/project/IM3/CLM meeting/Metrics/sample_data/Arrow_simulated.csv")

# Make sure that the two datasets have the same starting and finishing dates
observed_flow.shape[0]
simulated_flow.shape[0]

# First five lines of datasets 
observed_flow.head(5)
simulated_flow.head(5)

# Last five lines of datasets 
observed_flow.tail(5)
simulated_flow.tail(5)

# There are 50 years of gap in the start
observed_flow_short=observed_flow.iloc[(50*365+12):observed_flow.shape[0],:]
simulated_flow_short=simulated_flow.iloc[0:observed_flow_short.shape[0],:]

# Plot observed vs simulated

plt.style.use('seaborn-white')

fig_1, ax_fig_1=plt.subplots(figsize=[10,4])
plt.plot(range(0, observed_flow_short.shape[0]), observed_flow_short.iloc[:,3],  color="darkred", alpha=0.8)
plt.plot(range(0, simulated_flow_short.shape[0]), simulated_flow_short.iloc[:,3],  color="black", alpha=0.8)
ax_fig_1.set_xlabel('Days')
ax_fig_1.set_ylabel('Flow Discharge')
#ax_fig_1.set_facecolor('white')

flow_df=observed_flow_short
# Calculate flow duration curve

#--------------flow_duration_curve

# Input to metric calculation functions is daily and has the following format

#--------> Year  Month  Day  FLOW

fdc_df, slope_fdc=flow_duration_curve(flow_df)

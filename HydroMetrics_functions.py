# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 09:55:42 2021

@author: keyva
"""


import numpy as np
import pandas as pd



# Input to metric calculation functions is daily and has the following format

#--------> Year  Month  Day  FLOW


# Calculate flow duration curve
#--------------flow_duration_curve

def flow_duration_curve(flow_df, draw_plot=False):
    
    flow_ts=flow_df.iloc[:,3]
    df_flowdc=pd.DataFrame(np.zeros((flow_ts.shape[0],4)), columns=['flow_ts', 'rank', 'sorted_flow', 'exceedence_probability'])
    df_flowdc["flow_ts"]=flow_ts.values
    df_flowdc.loc[:,"rank"]=range(1, df_flowdc.shape[0]+1)
    df_flowdc.loc[:,"sorted_flow"]=flow_ts.sort_values(ascending=False).values
    df_flowdc.loc[:,"exceedence_probability"]=df_flowdc.loc[:,"rank"]/df_flowdc.shape[0]*100
    
    #
    high_limit=df_flowdc.loc[df_flowdc['exceedence_probability'] >= 59.999].index[0]
    low_limit=df_flowdc.loc[df_flowdc['exceedence_probability'] >= 32.999].index[0]
    
    slope_fdc=(np.log(df_flowdc.iloc[low_limit,2])-np.log(df_flowdc.iloc[high_limit,2]))/(0.66-0.33)
    
    return(df_flowdc, slope_fdc)


#----------------------runoff_ratio


def runoff_ratio(flow_df, p_df):
    
    p_ts=p_df.iloc[:,3]
    flow_ts=flow_df.iloc[:,3]
    Avg_runoff=flow_ts.mean()/p_ts.mean()
    
    return(Avg_runoff)


# ------------------ streamflow_elasticity


def streamflow_elasticity(flow_df, p_ts):
    
    flow_df.loc[:,"precip"]=p_ts.values
    
    m_df_date=flow_df.groupby(['Year'])
    agg_m_df_date=m_df_date.aggregate(np.mean)
    
    agg_m_df_date["P_change"]=0
    agg_m_df_date["Q_change"]=0
    agg_m_df_date["E_QP"]=0
    
    for i_yr in range(1, len(agg_m_df_date["precip"])):        
        agg_m_df_date.iloc[i_yr,4]=agg_m_df_date.iloc[i_yr,3]-agg_m_df_date.iloc[(i_yr-1),3]
        agg_m_df_date.iloc[i_yr,5]=agg_m_df_date.iloc[i_yr,2]-agg_m_df_date.iloc[(i_yr-1),2]
        agg_m_df_date.iloc[i_yr,6]=agg_m_df_date.iloc[i_yr,5]*agg_m_df_date.iloc[i_yr,3]/(agg_m_df_date.iloc[i_yr,4]*agg_m_df_date.iloc[i_yr,2])
  
    E_QP=np.median(agg_m_df_date.iloc[i_yr,6])
    
    return(E_QP)


#------------------ Snow day ratio


def snow_day_ratio(p_df, T_mean_df):
    
    p_ts=p_df.iloc[:,3]
    T_mean_ts=T_mean_df.iloc[:,3]
    threshold=2 # degree C
    N_P=p_ts[p_ts>0].count()
    N_S=p_ts[(p_ts>0) & (T_mean_ts>threshold)].count()
    
    R_SD=N_S/N_P
    
    return(R_SD)
    

# ----------- Q7_10

def Q7_10(flow_df):
    
    flow_ts=flow_df.iloc[:,3]
    moving_window=7 # days
    Ts_Q710=pd.DataFrame(np.zeros((flow_ts.shape[0],1)), columns=["Q7_10"])
    
    for i_day in range(0, len(flow_ts)):
        Ts_Q710.iloc[i_day,0]=np.mean(flow_ts.iloc[i_day:(i_day+moving_window)])
    
    y_df_date=flow_df.groupby(['Year'])
    agg_min_y_df_date=y_df_date.aggregate(np.min)
    
    df_Q7_10=pd.DataFrame(np.zeros((agg_min_y_df_date.shape[0],8)), columns=["Year", "min_7Q_flow", "rank", "Tr", "p_of_exc","Flow_sort", "Tr_sort", "P_sort"])
    df_Q7_10["Year"]=agg_min_y_df_date.index
    df_Q7_10["min_7Q_flow"]=agg_min_y_df_date.iloc[:,2].values
    df_Q7_10["rank"]=df_Q7_10["min_7Q_flow"].rank()
    df_Q7_10["Tr"]=(agg_min_y_df_date.shape[0]+1)/df_Q7_10["rank"].values # return period/time
    df_Q7_10["p_of_exc"]=1/df_Q7_10["Tr"].values
    df_Q7_10["Flow_sort"]=df_Q7_10["min_7Q_flow"].sort_values(ascending=False).values
    df_Q7_10["Tr_sort"]=df_Q7_10["Tr"].sort_values().values
    df_Q7_10["P_sort"]=df_Q7_10["p_of_exc"].sort_values(ascending=False).values
    
    limit=df_Q7_10.loc[df_Q7_10['Tr_sort'] >= 9.999].index[0]
    W_10F=df_Q7_10.iloc[limit,5]

    return(W_10F)
    



# High pulse count (HP): HP as the frequency of events that exceed the threshold of 2 times mean annual flow
# Flashiness index--> Richards-BakerFlashiness  Index  (abbreviated  as  R-B  Index),  

def R_B(flow_df):
    
    sum_num=0
    sum_den=0
    
    for i_day in range(1, len(flow_df["Year"])):        
        sum_num += abs(flow_df.iloc[i_day,3]-flow_df.iloc[(i_day-1),3])
        sum_den += flow_df.iloc[i_day,3]
    
    R_B_out=sum_num/sum_den
    
    return(R_B_out)


#----------------- MAF

def MAF(flow_df):
    
    y_df_date=flow_df.groupby(['Year'])
    agg_min_y_df_date=y_df_date.aggregate(np.mean)
    
    MAF=agg_min_y_df_date.iloc[:,2].mean()
    
    return(MAF)

#----------------- MSF

def MSF(flow_df):
    
    m_df_date=flow_df.groupby(['Month'])
    agg_min_m_df_date=m_df_date.aggregate(np.mean)
    
    MSF=agg_min_m_df_date.iloc[5:8,2].mean()
    
    return(MSF)


#------------- S15
# summer flow metrics---> frequency of low flow periods during summer


def S15(flow_df, MAF_value):
    
    df_date_flow=flow_df.iloc[:,3]
    MAF_value=MAF(flow_df)
    S15=df_date_flow[(flow_df.iloc[:,1]>5) & (flow_df.iloc[:,1]<9) & (flow_df.iloc[:,3]<0.15*MAF_value)].count()
    
    return(S15)
       
#------------- S15
# summer flow metrics---> frequency of high flow periods during summer
 #S95 (similar to W95), as flow events larger than this almost never occur in the summer in much of the region
     

def S_95(flow_df):
    
    qu_value=np.quantile(flow_df.iloc[:,3],0.95)
    #MAF_value=MAF(flow_df)
    df_date_flow=flow_df.iloc[:,3]
    S_95=df_date_flow[(flow_df.iloc[:,1]>5) & (flow_df.iloc[:,1]<9) & (flow_df.iloc[:,3]>qu_value)].count()
    
    return(S_95)


#------------------------ W95

def W_95(flow_df):
    
    qu_value=np.quantile(flow_df.iloc[:,3],0.95)
    df_date_flow=flow_df.iloc[:,3]
    W_95=df_date_flow[(flow_df.iloc[:,1]>11) & (flow_df.iloc[:,1]<3) & (flow_df.iloc[:,3]>qu_value)].count()
    
    return(W_95)

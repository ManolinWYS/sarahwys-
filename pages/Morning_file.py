
import streamlit as st
from streamlit.logger import get_logger
import io

import pandas as pd
from io import StringIO
from io import BytesIO
import os
import pandas as pd
from pandas.tseries.offsets import Day
from pandas.tseries.offsets import BDay
import numpy as np
from pandas import read_excel
from datetime import date, datetime
from functools import partial
import functools as ft
import re
import time

import pip
pip.main(["install", "openpyxl","XlsxWriter"])

#import openpyxl

def run():
    st.set_page_config(
        page_title="Morning file")

    st.write("#  Morning file")

    st.markdown(
        """
        Hi team, good morning! """
    )

if __name__ == "__main__":
    run()



TIME = st.selectbox(
    'Time setting',
    (' 09:00:00', ' 08:00:00'))

st.write('You selected:', TIME)


# TIME = " 09:00:00"
if datetime.today().isoweekday() == 1:
    start = str((datetime.now() - Day(3)).strftime("%Y-%m-%d")) + TIME
    end = str((datetime.now() - Day(2)).strftime("%Y-%m-%d")) + TIME
elif datetime.today().isoweekday() == 2: #Tuesday
    start = str((datetime.now() - Day(3)).strftime("%Y-%m-%d")) + TIME
    end = str((datetime.now()).strftime("%Y-%m-%d")) + TIME
else: 
    start = str((datetime.now() - BDay(1)).strftime("%Y-%m-%d")) + TIME
    end = str((datetime.now()).strftime("%Y-%m-%d")) + TIME

select_time = str(start + " to " + end)
st.write('The BO date range should start from ' + select_time)


rate = st.file_uploader("Please upload today's rate. If not uploaded, use yesterday's rate instead.")
if rate is not None: 
    rate = pd.read_csv(rate)



uploaded_BO = st.file_uploader("Please upload today's BO data")
if uploaded_BO is not None:
    BO = pd.read_excel(uploaded_BO)
    BO["Date"] = pd.to_datetime(BO["Date"], format='%d/%m/%Y %H:%M:%S')
    BO.sort_values(by='Date',  ascending = True,inplace = True)
    if datetime.today().isoweekday() == 1: #Monday
        start = str((datetime.now() - Day(3)).strftime("%Y-%m-%d")) + TIME
        end = str((datetime.now() - Day(2)).strftime("%Y-%m-%d")) + TIME
        BO = BO.loc[BO['Date'].between(start,end, inclusive='left')]

    elif datetime.today().isoweekday() == 2: #Tuesday
        start = str((datetime.now() - Day(3)).strftime("%Y-%m-%d")) + TIME
        end = str((datetime.now()).strftime("%Y-%m-%d")) + TIME
        BO = BO.loc[BO['Date'].between(start,end, inclusive='left')]
    
    else:
        start = str((datetime.now() - BDay(1)).strftime("%Y-%m-%d")) + TIME
        end = str((datetime.now()).strftime("%Y-%m-%d")) + TIME
        BO = BO.loc[BO['Date'].between(start,end, inclusive='left')]

    BO = pd.DataFrame(BO.loc[:,["ID","Date","Branch","Transaction type","Payment Method","Customer","Amount","Currency","Source","Recipient","Status","Comment"]])
    BO = BO.loc[BO["Transaction type"].str.contains("deposit|withdrawal|Reverse Withdrawal")]
    BO = BO.loc[BO["Status"].str.contains("Approved|Processing")]
    BO = BO.drop_duplicates(subset=['ID'], keep='first')
    BO["Customer"] = BO["Customer"].str.strip()
    BO['Customer'] = BO['Customer'].str.replace('  ', ' ')
    BO["Comment"] = BO["Comment"].str.strip()
    BO["Comment"] = BO["Comment"].fillna("NOINFO")
    BO.loc[BO["Comment"].str.contains("FSA"),"Branch"] = "FSA"
    BO.loc[BO["Comment"].str.contains("ASIC"),"Branch"] = "ASIC"
    BO.loc[BO["Comment"].str.contains("CySEC"),"Branch"] = "CySEC"
    FX = rate.iloc[:,[0,2]]
    BO = pd.merge(left = BO,
               right = FX,
              how = 'left',
              left_on = "Currency",
              right_on = "CCY")
    # BO["USD Equivalent"] = BO["USD Equivalent"]*BO["To USD"]
    SHARES_BO =  BO.loc[BO["Branch"].str.contains("Shares")]
    FSA_ICT_BO =  BO.loc[BO["Branch"].str.contains("FSA_ICT")]
    
    time = str((datetime.now() - BDay(1)).strftime("%d.%m"))
    BO_name="BO"+ time + ".xlsx"
    
    @st.cache_data
    def convert_df(df):
        return df.to_csv().encode('utf-8')
    BO = convert_df(BO)



    st.download_button(
    label="Download data as CSV",
    data=BO,
    file_name='BO.csv',
    mime='text/csv')




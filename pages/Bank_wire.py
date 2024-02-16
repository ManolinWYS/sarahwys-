import pandas as pd
from pandas.tseries.offsets import BDay
import numpy as np
from pandas import read_excel
from datetime import datetime
from functools import partial
import functools as ft
import re
import time
import os

import streamlit as st
from streamlit.logger import get_logger
import io


def run():
    st.set_page_config(
    page_title="Bank Wire")

    st.write("# :balloon: Bank Wire")

if __name__ == "__main__":
    run()


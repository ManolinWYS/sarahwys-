
import streamlit as st
from streamlit.logger import get_logger
import io
import pandas as pd
from io import StringIO

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




LOGGER = get_logger(__name__)



def run():
    st.set_page_config(
        page_title="Home Page",
        page_icon="👋",
    )

    st.write("# :balloon: Finance Team Homepage 👋")
   

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        **👈 Select a demo from the sidebar** to see some examples
        of what Streamlit can do!
        ### Want to learn more?
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)
        ### See more complex demos
        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )


if __name__ == "__main__":
    run()





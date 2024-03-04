import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import utils as utils



st.set_page_config(
    page_title = "Cricket World cup Project - Bowling Stats",
    layout="wide"
)

image_url = 'https://images.icc-cricket.com/icc-web/image/private/t_q-best/v1699648100/prd/assets/tournaments/cricketworldcup/extended-logo_gjruxa_zrvjhh.svg'

image_width = 800
image_height = 100
st.markdown(
    f"""
    <div style="display: flex; flex-direction: column; align-items: center; margin-top: 0px;
    margin-bottom: 50px;">
        <img src="{image_url}" style="width: {image_width}px; height: {image_height}px;">
    </div>  
    """,
    unsafe_allow_html=True,
    )

st.header("Bowling Stats", divider="gray")

balls = utils.balls
matches = utils.matches




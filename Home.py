import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import utils as utils



st.set_page_config(
    page_title = "Cricket World cup Project - Home" ,
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

image_url = "https://www.aljazeera.com/wp-content/uploads/2023/11/2023-11-19T165916Z_681108936_UP1EJBJ1B6PVQ_RTRMADP_3_CRICKET-WORLDCUP-IND-AUS-1700413267.jpg?resize=1170%2C780&quality=80"
image_width = 800
image_height = 400

# Set border color and width
border_color = "#16D9F9"
border_width = 5

st.markdown(
    f"""
        <div style="display: flex; justify-content: center; align-items: center; height: 50vh;">
            <img src="{image_url}" style="width:{image_width}px; height: {image_height}px; border: {border_width}px solid {border_color};">
        </div>
        """,
    unsafe_allow_html=True,
)

st.markdown(f'<h2 style="text-align: center;'
            f'"> Congratulations Australia </h2>',unsafe_allow_html=True,)
st.markdown(f'<h2 style="text-align: center;">ICC Mens World Cup 2023 Champions </h2>',unsafe_allow_html=True,)

import streamlit as st
import pandas as pd
import numpy as np

from utils import model
from sklearn.compose import ColumnTransformer
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler, RobustScaler
from sklearn.pipeline import Pipeline
import xgboost



st.set_page_config(
    page_title = "Cricket World cup Project - 1st Innings Score Predictor",
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

st.header("1st Innings Score Predictor", divider="gray")

model = model
teams = ["Australia", "Sri Lanka", "India", "England","South Africa", "Pakistan","Bangladesh", "Afghanistan", "Netherlands", "New Zealand"]

col1, col2 = st.columns(2)

batting_team = col1.selectbox("Batting team",["Australia", "Sri Lanka", "India", "England","South Africa", "Pakistan","Bangladesh", "Afghanistan", "Netherlands", "New Zealand"])
bowling_team = col2.selectbox("Bowling team",["Australia", "Sri Lanka", "India", "England","South Africa", "Pakistan","Bangladesh", "Afghanistan", "Netherlands", "New Zealand"])
venue = col1.selectbox("Venue",["Arun Jaitley Stadium", "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium", "Eden Gardens",
         "Himachal Pradesh Cricket Association Stadium", "M Chinnaswamy Stadium", "MA Chidambaram Stadium, Chepauk", "Maharashtra Cricket Association Stadium",
         "Rajiv Gandhi International Stadium, Uppal", "Wankhede Stadium","Narendra Modi Stadium, Ahmedabad"])


current_score = col2.number_input("Enter current Runs", min_value = 0)
wickets = col1.number_input("Enter No of wickets", min_value = 0, max_value =10)
over_num = col1.number_input("Enter current Over", min_value = 0, max_value =50)
last_30_balls = col2.number_input("Enter last 5 overs Runs",min_value = 0)
ball_num = col2.number_input("Enter current Ball of Over", min_value = 0, max_value =6)

button = st.button("Predict Score")
if button:
    try:
        run_rate = (current_score * 6) / ((over_num*6) + ball_num)
        balls_left = 300 - ((over_num*6) + ball_num)
        wickets_left = 10 - wickets
        rr_in_last_30_overs = last_30_balls/5

        pred = pd.DataFrame(columns=['batting_team','bowling_team',	'venue'	,'current_score','run_rate',
                                    'balls_left','wickets_left','runs_in_last_30_balls','rr_in_last_30_overs'])

        new_data = {
            'batting_team': batting_team,
            'bowling_team': bowling_team,
            'venue': venue,
            'current_score': current_score,
            'run_rate': run_rate,
            'balls_left': balls_left,
            'wickets_left': wickets_left,
            'runs_in_last_30_balls': last_30_balls,
            'rr_in_last_30_overs': rr_in_last_30_overs
        }

        pred.loc[len(pred)] = new_data
        
        value = model.predict(pred)[0]
        st.subheader(f"The Predicted Score of {batting_team} should be between {int(value) - 10} - {int(value) + 10}")

    except:
        st.subheader("At least 5 overs must have bowled to get the prediction")

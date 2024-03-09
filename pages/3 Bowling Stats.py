import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import utils 

plt.rcParams['figure.figsize']=(10,7)


st.set_page_config(
    page_title = "Cricket World cup Project - Batting Stats",
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



balls = utils.balls
matches = utils.matches



def color_scheme(value_counts):
    colors = []
    for i in value_counts:
        if i == value_counts.max():
            colors.append('#0096D2')
        else:
            colors.append('#FF00A5')

    return colors

teams = ["All"]
teams.extend(sorted(balls.batting_team.unique()))
selected_team = st.sidebar.selectbox("Select Team",teams)

st.header(f"Bowling Stats - {selected_team}", divider="grey")




st.subheader("BEST BOWLING FIGURE")
col1, col2 = st.columns(2)
with col1:
    best_figure = utils.best_figure(balls , selected_team=selected_team)

    fig, ax = plt.subplots()
    fig, ax = utils.plot_look(fig, ax)

    sns.barplot(x=np.arange(best_figure.head().shape[0]),
                y=best_figure["is_wicket"].head(),
                palette=color_scheme(best_figure["is_wicket"].head()),
                edgecolor="gold", width=0.8
                )

    ax.set_xlabel("Bowler", color="#320073", fontdict={"fontsize": "x-large"})
    ax.set_ylabel("Figure", color="#320073", fontdict={"fontsize": "x-large"})
    ax.set_xticklabels(best_figure['bowler'].head(), color="w", rotation=25, ha='right', fontdict={"fontsize": "x-large"})
    ax.set_yticklabels(ax.get_yticks(), color="#320073")
    ax.set_xlim(-1, 5)
    ax.set_ylim(0, best_figure["is_wicket"].max() + 1)

    for index, (wickets, figure) in enumerate(zip(best_figure["is_wicket"].head(), best_figure["figure"].head())):
        plt.text(index, wickets, figure,
                 ha='center', va='bottom', color="white", fontdict={"fontsize": "x-large"})
    st.pyplot(fig)
with col2:
    st.dataframe(best_figure[["bowler", "figure"]]. \
                 rename(columns={"figure": 'Figures', "bowler": "Bowler"}).set_index("Bowler"), width=300)

st.subheader("BEST BOWLING AVERAGE")
col1, col2 = st.columns(2)
with col1:
    bowling_average = utils.bowling_avg(balls , selected_team=selected_team)

    fig, ax = plt.subplots()
    fig, ax = utils.plot_look(fig, ax)

    sns.barplot(x=np.arange(bowling_average.head().shape[0]),
                y=bowling_average["average"].head(),
                palette= ["#0096D2", "#FF00A5",'#FF00A5', "#FF00A5", "#FF00A5"],
                edgecolor="gold", width=0.8
                )

    ax.set_xlabel("", fontdict={"fontsize": "x-large"})
    ax.set_ylabel("",  fontdict={"fontsize": "x-large"})
    ax.set_xticklabels(bowling_average['bowler'].head(), color="w", rotation=25, ha='right', fontdict={"fontsize": "x-large"})
    ax.set_yticklabels(ax.get_yticks(), color="#320073")
    ax.set_xlim(-1, 5)
    ax.set_ylim(0, bowling_average["average"].head().max()+5)

    for index, value in enumerate(bowling_average["average"].head()):
        plt.text(index, np.round(value, 2) + 0.2, str(np.round(value, 2)),
                ha='center', va='bottom', color="white", fontdict={"fontsize": "x-large"})
    st.pyplot(fig)    
with col2:
    st.dataframe(bowling_average[["bowler", "average"]]. \
                 rename(columns={"average": 'Average', "bowler": "Bowler"}).set_index("Bowler"), width=300)
    
st.subheader("BEST BOWLING STRIKE RATE INNINGS")
col1, col2 = st.columns(2)
with col1:
    bowling_sr_inn = utils.sr_bowling_inn(balls , selected_team=selected_team)

    fig, ax = plt.subplots()
    fig, ax = utils.plot_look(fig, ax)

    sns.barplot(x=np.arange(bowling_sr_inn.head().shape[0]),
                y=bowling_sr_inn["sr"].head(),
                palette= ["#0096D2", "#FF00A5",'#FF00A5', "#FF00A5", "#FF00A5"],
                edgecolor="gold", width=0.8
                )

    ax.set_xlabel("", fontdict={"fontsize": "x-large"})
    ax.set_ylabel("",  fontdict={"fontsize": "x-large"})
    ax.set_xticklabels(bowling_sr_inn['bowler'].head(), color="w", rotation=25, ha='right', fontdict={"fontsize": "x-large"})
    ax.set_yticklabels(ax.get_yticks(), color="#320073")
    ax.set_xlim(-1, 5)
    ax.set_ylim(0, bowling_sr_inn["sr"].head().max()+5)

    for index, value in enumerate(bowling_sr_inn["sr"].head()):
        plt.text(index, np.round(value, 2) + 0.2, str(np.round(value, 2)),
                ha='center', va='bottom', color="white", fontdict={"fontsize": "x-large"})
    st.pyplot(fig)   
with col2:
    st.dataframe(bowling_sr_inn[["bowler", "sr"]].rename(columns={"sr": 'Strike Rate', "bowler": "Bowler"}).set_index("Bowler"), width=300)  

    
st.subheader("BEST BOWLING STRIKE RATE TOURNAMENT")
col1, col2 = st.columns(2)
with col1:
    bowling_sr = utils.sr_bowling(balls , selected_team=selected_team)

    fig, ax = plt.subplots()
    fig, ax = utils.plot_look(fig, ax)

    sns.barplot(x=np.arange(bowling_sr.head().shape[0]),
                y=bowling_sr    ["sr"].head(),
                palette= ["#0096D2", "#FF00A5",'#FF00A5', "#FF00A5", "#FF00A5"],
                edgecolor="gold", width=0.8
                )

    ax.set_xlabel("", fontdict={"fontsize": "x-large"})
    ax.set_ylabel("",  fontdict={"fontsize": "x-large"})
    ax.set_xticklabels(bowling_sr['bowler'].head(), color="w", rotation=25, ha='right', fontdict={"fontsize": "x-large"})
    ax.set_yticklabels(ax.get_yticks(), color="#320073")
    ax.set_xlim(-1, 5)
    ax.set_ylim(0, bowling_sr["sr"].head().max()+5)

    for index, value in enumerate(bowling_sr["sr"].head()):
        plt.text(index, np.round(value, 2) + 0.2, str(np.round(value, 2)),
                ha='center', va='bottom', color="white", fontdict={"fontsize": "x-large"})
    st.pyplot(fig)   
with col2:
    st.dataframe(bowling_sr[["bowler", "sr"]].rename(columns={"sr": 'Strike Rate', "bowler": "Bowler"}).set_index("Bowler"), width=300)   

st.subheader("BEST ECONOMY INNINGS")
col1, col2 = st.columns(2)
with col1:
    economy_inn = utils.economy_inng(balls , selected_team=selected_team)

    fig, ax = plt.subplots()
    fig, ax = utils.plot_look(fig, ax)

    sns.barplot(x=np.arange(economy_inn.head().shape[0]),
                y=economy_inn["economy"].head(),
                palette= ["#0096D2", "#FF00A5",'#FF00A5', "#FF00A5", "#FF00A5"],
                edgecolor="gold", width=0.8
                )

    ax.set_xlabel("", fontdict={"fontsize": "x-large"})
    ax.set_ylabel("",  fontdict={"fontsize": "x-large"})
    ax.set_xticklabels(economy_inn['bowler'].head(), color="w", rotation=25, ha='right', fontdict={"fontsize": "x-large"})
    ax.set_yticklabels(ax.get_yticks(), color="#320073")
    ax.set_xlim(-1, 5)
    ax.set_ylim(0, economy_inn["economy"].head().max()+1)

    for index, value in enumerate(economy_inn["economy"].head()):
        plt.text(index, np.round(value, 2) + 0.2, str(np.round(value, 2)),
                ha='center', va='bottom', color="white", fontdict={"fontsize": "x-large"})
    st.pyplot(fig)    
with col2:
    st.dataframe(economy_inn[["bowler", "economy"]]. \
                 rename(columns={"economy": 'Economy', "bowler": "Bowler"}).set_index("Bowler"), width=300)
    
st.subheader("BEST ECONOMY TOURNAMENT")
col1, col2 = st.columns(2)
with col1:
    economy = utils.economy(balls , selected_team=selected_team)

    fig, ax = plt.subplots()
    fig, ax = utils.plot_look(fig, ax)

    sns.barplot(x=np.arange(economy.head().shape[0]),
                y=economy["economy"].head(),
                palette= ["#0096D2", "#FF00A5",'#FF00A5', "#FF00A5", "#FF00A5"],
                edgecolor="gold", width=0.8
                )

    ax.set_xlabel("", fontdict={"fontsize": "x-large"})
    ax.set_ylabel("",  fontdict={"fontsize": "x-large"})
    ax.set_xticklabels(economy['bowler'].head(), color="w", rotation=25, ha='right', fontdict={"fontsize": "x-large"})
    ax.set_yticklabels(ax.get_yticks(), color="#320073")
    ax.set_xlim(-1, 5)
    ax.set_ylim(0, economy["economy"].head().max()+1)

    for index, value in enumerate(economy["economy"].head()):
        plt.text(index, np.round(value, 2) + 0.2, str(np.round(value, 2)),
                ha='center', va='bottom', color="white", fontdict={"fontsize": "x-large"})
    st.pyplot(fig)    
with col2:
    st.dataframe(economy[["bowler", "economy"]]. \
                 rename(columns={"economy": 'Economy', "bowler": "Bowler"}).set_index("Bowler"), width=300)
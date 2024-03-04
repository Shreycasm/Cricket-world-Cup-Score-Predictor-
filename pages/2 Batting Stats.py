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


teams = li = ["All"]
li.extend(sorted(balls.batting_team.unique()))
selected_team = st.sidebar.selectbox("Select Team",teams)

st.header(f"Batting Stats - {selected_team}", divider="grey")


st.subheader("Highest Score Innings")
col1 , col2 = st.columns(2)
with (col1):
    highest_score_df = utils.highest_score(balls,selected_team=selected_team)

    fig, ax = plt.subplots()
    fig , ax = utils.plot_look(fig, ax)

    sns.barplot(x=np.arange(highest_score_df.head().shape[0]),
                y=highest_score_df["batsmen_runs"].head(),
                palette=color_scheme(highest_score_df["batsmen_runs"].head()),
                edgecolor="gold", width=0.8, ci=False
                )



    ax.set_xlabel("Batsmen", color="w",fontdict = {"fontsize": "x-large"})
    ax.set_ylabel("Runs", color="w",fontdict = {"fontsize": "x-large"})
    ax.set_xticklabels(highest_score_df['batsmen'].head(), color="w", rotation=25,fontdict = {"fontsize": "x-large"})
    ax.set_yticklabels(ax.get_yticks(), color="#320073")
    ax.set_xlim(-1, 5)
    ax.set_ylim(0, highest_score_df["batsmen_runs"].max() + 20)
    

    for index, value in enumerate(highest_score_df["batsmen_runs"].head()):
        plt.text(index, value + 0.2, str(value), ha='center', va='bottom', color="white",
                 fontdict = {"fontsize": "x-large"})

    st.pyplot(fig)
with col2:
    st.dataframe(highest_score_df[["batsmen", "batsmen_runs"]]. \
                 rename(columns={"batsmen_runs": 'Runs', "batsmen": "Batsmen"}).set_index("Batsmen"), width=350)


st.subheader("Most Runs")
col1, col2 = st.columns(2)
with col1:

    most_runs = utils.most_runs(balls,selected_team=selected_team)

    fig, ax = plt.subplots()
    fig , ax = utils.plot_look(fig, ax)

    sns.barplot(x=np.arange(most_runs.head().shape[0]),
                y=most_runs["batsmen_runs"].head(),
                palette=color_scheme(most_runs["batsmen_runs"].head()),
                edgecolor="gold", width=0.8
                )

    ax.set_xlabel("Batsmen", color="w",fontdict = {"fontsize": "x-large"})
    ax.set_ylabel("Runs", color="w",fontdict = {"fontsize": "x-large"})
    ax.set_xticklabels(most_runs['batsmen'].head(), color="w", rotation=25,fontdict = {"fontsize": "x-large"})
    ax.set_yticklabels(ax.get_yticks(), color="#320073")
    ax.set_xlim(-1, 5)
    ax.set_ylim(0, most_runs["batsmen_runs"].max() + 100)
    

    for index, value in enumerate(most_runs["batsmen_runs"].head()):
        plt.text(index, value + 0.2, str(value), ha='center', va='bottom', color="white",
                 fontdict = {"fontsize": "x-large"})

    st.pyplot(fig)
with col2:
    st.dataframe(most_runs[["batsmen", "batsmen_runs"]]. \
                 rename(columns={"batsmen_runs": 'Runs', "batsmen": "Batsmen"}).set_index("Batsmen"), width=350)


st.subheader("Most 4s")
col1, col2 = st.columns(2)
with col1:
    most_4s = utils.most_4s(balls,selected_team=selected_team)

    fig, ax = plt.subplots()
    fig , ax = utils.plot_look(fig, ax)

    sns.barplot(x=np.arange(most_4s.head().shape[0]),
                y=most_4s["batsmen_runs"].head(),
                palette=color_scheme(most_4s["batsmen_runs"].head()),
                edgecolor="gold", width=0.8
                )
    ax.set_xlabel("Batsmen", color="w",fontdict = {"fontsize": "x-large"})
    ax.set_ylabel("No. of 4s", color="w",fontdict = {"fontsize": "x-large"})
    ax.set_xticklabels(most_4s['batsmen'].head(), color="w", rotation=25,fontdict = {"fontsize": "x-large"})
    ax.set_yticklabels(ax.get_yticks(), color="#320073")
    ax.set_xlim(-1, 5)
    ax.set_ylim(0, most_4s["batsmen_runs"].max() + 10)


    for index, value in enumerate(most_4s["batsmen_runs"].head()):
        plt.text(index, value + 0.2, str(value), ha='center', va='bottom', color="white",
                 fontdict = {"fontsize": "x-large"})

    st.pyplot(fig)
with col2:
    st.dataframe(most_4s[["batsmen", "batsmen_runs"]]. \
                 rename(columns={"batsmen_runs": '4S', "batsmen": "Batsmen"}).set_index("Batsmen"), width=350)


st.subheader("Most 6s")
col1, col2 = st.columns(2)
with col1:

    most_6s = utils.most_6s(balls,selected_team=selected_team)

    fig, ax = plt.subplots()
    fig , ax = utils.plot_look(fig, ax)

    sns.barplot(x=np.arange(most_6s.head().shape[0]),
                y=most_6s["batsmen_runs"].head(),
                palette=color_scheme(most_6s["batsmen_runs"].head()),
                edgecolor="gold", width=0.8
                )
    ax.set_xlabel("Batsmen", color="w",fontdict = {"fontsize": "x-large"})
    ax.set_ylabel("No. of 6s", color="w",fontdict = {"fontsize": "x-large"})
    ax.set_xticklabels(most_6s['batsmen'].head(), color="w", rotation=25,fontdict = {"fontsize": "x-large"})
    ax.set_yticklabels(ax.get_yticks(), color='#320073')
    ax.set_xlim(-1, 5)
    ax.set_ylim(0, most_6s["batsmen_runs"].max() + 5)
   

    for index, value in enumerate(most_6s["batsmen_runs"].head()):
        plt.text(index, value + 0.2, str(value), ha='center', va='bottom', color="white",
                 fontdict = {"fontsize": "x-large"})

    st.pyplot(fig)
with col2:
    st.dataframe(most_6s[["batsmen", "batsmen_runs"]]. \
                 rename(columns={"batsmen_runs": '6S', "batsmen": "Batsmen"}).set_index("Batsmen"), width=350)


st.subheader("Best Strike Rate In Tournament")
col1, col2 = st.columns(2)
with col1:
    sr = utils.sr(balls, selected_team=selected_team)

    fig, ax = plt.subplots()
    fig , ax = utils.plot_look(fig, ax)

    sns.barplot(x=np.arange(sr.head().shape[0]),
                y=sr["strike_rate"].head(),
                palette=color_scheme(sr["strike_rate"].head()),
                edgecolor="gold", width=0.8
                )

    ax.set_xlabel("Batsmen", color="w",fontdict = {"fontsize": "x-large"})
    ax.set_ylabel("Strike Rate", color="w",fontdict = {"fontsize": "x-large"})
    ax.set_xticklabels(sr['batsmen'].head(), color="w", rotation=25,fontdict = {"fontsize": "x-large"})
    ax.set_yticklabels(ax.get_yticks(), color="#320073")
    ax.set_xlim(-1, 5)
    ax.set_ylim(0, sr["strike_rate"].max() + 25)
    

    for index, value in enumerate(sr["strike_rate"].head()):
        plt.text(index, np.round(value, 2), str(np.round(value, 2)),
                 ha='center', va='bottom', color="white",fontdict = {"fontsize": "x-large"})

    st.pyplot(fig)
with col2:
    st.dataframe(sr[["batsmen", "strike_rate"]]. \
                 rename(columns={"strike_rate": 'Strike Rate', "batsmen": "Batsmen"}).set_index("Batsmen"), width=350)


st.subheader("Best Strike Rate Innings")
col1, col2 = st.columns(2)
with col1:
    sr_inng = utils.sr_inng(balls,selected_team= selected_team)

    fig, ax = plt.subplots()
    fig , ax = utils.plot_look(fig, ax)

    sns.barplot(x=np.arange(sr_inng.head().shape[0]),
                y=sr_inng["strike_rate"].head(),
                palette=color_scheme(sr_inng["strike_rate"].head()),
                edgecolor="gold", width=0.8
                )

    ax.set_xlabel("Batsmen", color="w",fontdict = {"fontsize": "x-large"})
    ax.set_ylabel("Strike Rate", color="w",fontdict = {"fontsize": "x-large"})
    ax.set_xticklabels(sr_inng['batsmen'].head(), color="w", rotation=25,fontdict = {"fontsize": "x-large"})
    ax.set_yticklabels(ax.get_yticks(), color="#320073")
    ax.set_xlim(-1, 5)
    ax.set_ylim(0, sr_inng["strike_rate"].max() + 50)
    
    for index, value in enumerate(sr_inng["strike_rate"].head()):
        plt.text(index, np.round(value, 2) + 0.2, str(np.round(value, 2)),
                 ha='center', va='bottom', color="white",fontdict = {"fontsize": "x-large"})

    st.pyplot(fig)
with col2:
    st.dataframe(sr_inng[["batsmen", "strike_rate"]]. \
                 rename(columns={"strike_rate": 'Strike Rate', "batsmen": "Batsmen"}).set_index("Batsmen"), width=350)


st.subheader("Best Batting Average")
col1, col2 = st.columns(2)
with col1:
    average = utils.average(balls, selected_team=selected_team)

    fig, ax = plt.subplots()
    fig , ax = utils.plot_look(fig, ax)

    sns.barplot(x=np.arange(average.head().shape[0]),
                y=average["avg"].head(),
                palette=color_scheme(average["avg"].head()),
                edgecolor="gold", width=0.8
                )

    ax.set_xlabel("Batsmen", color="w",fontdict = {"fontsize": "x-large"})
    ax.set_ylabel("Average", color="w",fontdict = {"fontsize": "x-large"})
    ax.set_xticklabels(average['batsmen'].head(), color="w", rotation=25,fontdict = {"fontsize": "x-large"})
    ax.set_yticklabels(ax.get_yticks(), color="#320073")
    ax.set_xlim(-1, 5)
    ax.set_ylim(0, average["avg"].max() + 10)
    

    for index, value in enumerate(average["avg"].head()):
        plt.text(index, np.round(value, 2) + 0.2, str(np.round(value, 2)),
                 ha='center', va='bottom', color="white",fontdict = {"fontsize": "x-large"})

    st.pyplot(fig)
with col2:
    st.dataframe(average[["batsmen", "avg"]], width=350, hide_index =True)


st.subheader("Most 50s")
col1, col2 = st.columns(2)
with col1:
    most_50s = utils.most_50s(balls, selected_team=selected_team)

    fig, ax = plt.subplots()
    fig , ax = utils.plot_look(fig, ax)

    sns.barplot(x=np.arange(most_50s.head().shape[0]),
                y=most_50s["batsmen_runs"].head(),
                palette=color_scheme(most_50s["batsmen_runs"].head()),
                edgecolor="gold", width=0.8
                )

    ax.set_xlabel("Batsmen", color="w",fontdict = {"fontsize": "x-large"})
    ax.set_ylabel("No. of 50s", color="w",fontdict = {"fontsize": "x-large"})
    ax.set_xticklabels(most_50s['batsmen'].head(), color="w", rotation=25,fontdict = {"fontsize": "x-large"})
    ax.set_yticklabels(ax.get_yticks(), color='#320073')
    ax.set_xlim(-1, 5)
    

    for index, value in enumerate(most_50s["batsmen_runs"].head()):
        plt.text(index, np.round(value, 2) + 0.2, str(np.round(value, 2)),
                 fontdict = {"fontsize": "x-large"},ha='center', va='bottom', color="white")

    st.pyplot(fig)
with col2:
    st.dataframe(most_50s[["batsmen", "batsmen_runs"]]. \
                 rename(columns={"batsmen_runs": 'No. of 50s', "batsmen": "Batsmen"}).set_index("Batsmen"), width=350)


st.subheader("Most 100s")
col1, col2 = st.columns(2)
with col1:
    most_100s = utils.most_100s(balls, selected_team=selected_team)
    fig, ax = plt.subplots()
    fig , ax = utils.plot_look(fig, ax)
    try:
        sns.barplot(x=np.arange(most_100s.head().shape[0]),
                    y=most_100s["batsmen_runs"].head(),
                    palette=color_scheme(most_100s["batsmen_runs"].head()),
                    edgecolor="gold", width=0.8
                    )

        ax.set_xlabel("Batsmen", color="w",fontdict = {"fontsize": "x-large"})
        ax.set_ylabel("No. of 100s", color="w",fontdict = {"fontsize": "x-large"})
        ax.set_xticklabels(most_100s['batsmen'].head(), color="w", rotation=25,fontdict = {"fontsize": "x-large"})
        ax.set_yticklabels(ax.get_yticks(), color= "#320073",fontdict = {"fontsize": 0.0})
        ax.set_xlim(-1, 5)
        ax.set_ylim(0, most_100s["batsmen_runs"].max() + 1)
       

        for index, value in enumerate(most_100s["batsmen_runs"].head()):
            plt.text(index, np.round(value, 2) + 0.2, str(np.round(value, 2)),
                     ha='center', va='bottom', color="white",fontdict = {"fontsize": "x-large"})

        st.pyplot(fig)
    except:
        st.write(f"{selected_team} has no individual century")
with col2:
    try:
        st.dataframe(most_100s[["batsmen", "batsmen_runs"]]. \
                     rename(columns={"batsmen_runs": 'No. of 100s', "batsmen": "Batsmen"}).set_index("Batsmen"),
                     width=350)
    except:

        st.write(f"{selected_team} has no individual century")
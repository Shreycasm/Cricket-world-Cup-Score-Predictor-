import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import utils as utils


st.set_page_config(
    page_title = "Cricket World cup Project - Overall Analysis",
    layout="wide"
                )

plt.rcParams['figure.figsize']=(12,10)



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

st.header("OverAll Stats", divider="gray")


## METRICS
col1 , col2 , col3 , col4 , col5 = st.columns(5)
with col1:
    st.metric(value = balls.match_id.nunique() , label="Total matches")
with col2:
    st.metric(value=balls.total_runs.sum(), label="Total Runs")
with col3:
    st.metric(value=balls.is_wicket.sum(), label="Total Wickets")
with col4:
    st.metric(value=balls[balls.batsmen_runs == 6].shape[0], label="Total 6s")
with col5:
    st.metric(value=balls[balls.batsmen_runs == 4].shape[0], label="Total 4s")

col1 , col2 , col3, col4, col5 =  st.columns(5)
with col1:
    pass
with col2:
    most_50s = utils.most_50s(balls)
    st.metric(value=most_50s["batsmen_runs"].sum(), label="No. of 50s")
with col3:
    most_100s = utils.most_100s(balls)
    st.metric(value=most_100s["batsmen_runs"].sum(), label="No. of 100s")
with col4:
    matches_played = matches[(matches["team_1"] == "India") | (matches["team_2"] == "India")].shape[0]
    matches_won = matches[((matches["team_1"] == "India") | (matches["team_2"] == "India")) & (
            matches["match_winner"] == "India")].shape[0]
    st.metric(value=f'{np.round((matches_won / matches_played) * 100, 1)}%', label="Best Win %")
with col5:
    pass

st.divider()


col1 , col2 , col3 = st.columns(3)
with col1:
    st.metric(value = balls.groupby('batsmen')["batsmen_runs"].sum().sort_values(ascending =False).head(1),
            label =f"Most runs \n\n {balls.groupby('batsmen')['batsmen_runs'].sum().sort_values(ascending =False).head(1).index[0]}")
with col2:
    st.metric(value = balls.groupby('bowler')["is_wicket"].sum().sort_values(ascending =False).head(1),
            label =f"Most Wickets \n \n{balls.groupby('bowler')['is_wicket'].sum().sort_values(ascending =False).head(1).index[0]}")
with col3:
    st.metric(value = balls.groupby(["match_id" , 'batsmen'])["batsmen_runs"].sum().sort_values(ascending =False).head(1),
            label =f"Highest Individual Score \n \n{balls.groupby(['match_id' , 'batsmen'])['batsmen_runs'].sum().sort_values(ascending =False).head(1).index[0][1]}")

col1, col2, col3 = st.columns(3)
with col1 :
    innnnnn = balls[balls["inning_no"] == 1]
    innnnnn = innnnnn.groupby(["match_id", "batting_team"]).agg(
        {'total_runs': 'sum', "is_wicket": "sum"}).reset_index(). \
        sort_values(by="total_runs", ascending=False)
    innnnnn["final_score"] = innnnnn["total_runs"].astype("str") + "/" + innnnnn["is_wicket"].astype("str")
    st.metric(value=innnnnn["final_score"].iloc[0], label=f'Highest Inning Score \n\n{innnnnn["batting_team"].iloc[0]}')
with col2:
    innggg2 = balls.groupby(["match_id"]).agg({'total_runs': 'sum'}).reset_index().sort_values(by="total_runs", ascending=False)
    innggg2[["team_1", "team_2"]] = matches[matches["match_id"].isin(innggg2["match_id"].tolist())][["team_1", "team_2"]]
    innggg2["vs"] = innggg2["team_1"]+ str(" vs ") + innggg2["team_2"] 
    st.metric(value=innggg2["total_runs"].iloc[0], label=f'Most Runs in a Match \n\n{innggg2["vs"].iloc[0]}')


st.divider()

st.subheader("MOST WINS")
col1 , col2 = st.columns(2)
with col1:
    most_wins =utils.mot_matches_won(matches)

    fig ,ax = plt.subplots()
    fig , ax =utils.plot_look(fig , ax)

    plt.barh(most_wins['Team'], most_wins["No of Wins"] , edgecolor ="gold", color = utils.color_scheme(most_wins["No of Wins"]))

    ax.set_yticklabels(most_wins["Team"], color="w", fontdict={"fontsize":"xx-large"})
    ax.set_xticklabels(ax.get_xticks(), color ="#320073")

    for i, value in enumerate(most_wins['No of Wins']):
        ax.text(value + 0.1, i, str(value), va='center',color="w",fontdict = {"fontsize": "xx-large"})

    st.pyplot(fig)
with col2:
    st.dataframe(most_wins, hide_index= True, width =300)

st.subheader("MOST TOSS WON")
col1 , col2 = st.columns(2)
with col1:
    most_wins =utils.most_toss_won(matches)

    fig ,ax = plt.subplots()
    fig , ax =utils.plot_look(fig , ax)

    plt.barh(most_wins['Team'], most_wins["No of Wins"] , edgecolor ="gold", color = utils.color_scheme(most_wins["No of Wins"]))

    ax.set_yticklabels(most_wins["Team"], color="w", fontdict={"fontsize":"xx-large"})
    ax.set_xticklabels(ax.get_xticks(), color ="#320073")

    for i, value in enumerate(most_wins['No of Wins']):
        ax.text(value + 0.1, i, str(value), va='center',color="w",fontdict = {"fontsize": "xx-large"})

    st.pyplot(fig)
with col2:
    st.dataframe(most_wins, hide_index= True, width =300)

col1,  col2 = st.columns(2) ## TOSS DECISION & MATCH RESULT AFTER WINNING TOSS
with col1:
    st.subheader("TOSS DECISION")
    fig , ax = plt.subplots()
    fig , ax = utils.plot_look(fig, ax)
    decision  = utils.toss_decision(matches)
    plt.pie(decision["count"], colors =["#0096D2", "#FF00A5"], autopct ="%.2f%%", labels=["Field", "Bat"],
            wedgeprops=dict(edgecolor='gold'),
            textprops={'color': "w",'fontsize': 30 })
    plt.pie([360], colors =["#320073"], radius =0.8,wedgeprops=dict(edgecolor='gold'),)

    

    st.pyplot(fig)
with col2:
    st.subheader("WIN % AFTER WINNING TOSS")
    fig , ax = plt.subplots()
    fig , ax = utils.plot_look(fig, ax)
    value  = utils.toss_win_match_win(matches)
    plt.pie([value , 100-value] ,colors =["#0096D2", "#FF00A5"], autopct ="%.0f%%", labels=["Won match", "Lost Match"],
            wedgeprops=dict(edgecolor='gold'),
            textprops={'color': "w",'fontsize': 30 })
    plt.pie([360], colors =["#320073"], radius =0.8,wedgeprops=dict(edgecolor='gold'),)

    

    st.pyplot(fig)

    
st.subheader("TOSS DECISION BY EACH VENUE")
col1 , col2 = st.columns(2)
with col1:
    df =utils.toss_decision_by_venue(matches)

    fig, ax = plt.subplots()
    fig , ax =utils.plot_look(fig , ax)

    bar_position_team = np.arange(len(df))

    ax.barh(bar_position_team, df['Bat'], label='Bat',edgecolor="gold")
    ax.barh(bar_position_team, (df['Field'] * -1), label='Field', color='#FF00A5',edgecolor="gold")


    ax.set_yticks(bar_position_team)
    ax.set_yticklabels(df.City, color="w",fontdict = {"fontsize": "xx-large"})
    ax.set_xticklabels(ax.get_xticks(), color="#320073")
    
    legend = plt.legend(fontsize = "xx-large")
    legend.get_frame().set_facecolor('#320073')
    legend.get_frame().set_edgecolor('white')
    plt.setp(legend.get_texts(), color='w')



    for i, value in enumerate(df['Bat'].astype("int")):
        ax.text(value + 0.1, i, str(value), va='center',color="w",fontdict = {"fontsize": "xx-large"})

    for i, value in enumerate(df['Field'].astype("int")):
        ax.text(-value - 0.1, i, str(value), va='center', ha='right', color="w",fontdict = {"fontsize": "xx-large"})
    st.pyplot(fig)
with col2:
    st.dataframe(df, width=300, hide_index=True)


st.subheader("AVERAGE 1ST INNINGS SCORE AT DIFFERENT VENUE")
col1, col2 = st.columns(2)
with col1:
    df = utils.average_score_venue(matches, balls)
    fig, ax = plt.subplots()
    fig, ax = utils.plot_look(fig, ax)

    plt.bar(df["City"], df["Avg. Score"], color =utils.color_scheme(df["Avg. Score"]), edgecolor="gold")

    ax.set_xticklabels(df.City, color="w",fontdict = {"fontsize": "xx-large"},rotation =25)
    ax.set_yticklabels(ax.get_xticks(), color="#320073", )

    for i, value in enumerate(df["Avg. Score"]):
            ax.text(i, int(value)+ 0.2, str(int(value)),
                    ha='center', va='bottom', color="white",fontdict = {"fontsize": "x-large"})

    st.pyplot(fig)
with col2:
    st.dataframe(df, hide_index=True, width =300)

st.subheader("MOST 50+ INDIVIDUAL SCORES")
col1, col2 =st.columns(2)
with col1:
    most_100_team , most_50_team = utils.most_100_n_50_team(balls)

    fig, ax = plt.subplots()
    fig , ax =utils.plot_look(fig , ax)

    bar_position_team = np.arange(len(most_100_team))

    ax.barh(bar_position_team, most_50_team['50s'], label='50',edgecolor="gold")
    ax.barh(bar_position_team, (most_100_team['100s'] * -1), label='100s', color='#FF00A5',edgecolor="gold")


    ax.set_yticks(bar_position_team)
    ax.set_yticklabels(most_50_team.Team, color="w",fontdict = {"fontsize": "xx-large"})
    ax.set_xticklabels(ax.get_xticks(), color="#320073")
    
    legend = plt.legend(fontsize = "xx-large")
    legend.get_frame().set_facecolor('#320073')
    legend.get_frame().set_edgecolor('white')
    plt.setp(legend.get_texts(), color='w')



    for i, value in enumerate(most_50_team['50s']):
        ax.text(value + 0.1, i, str(value), va='center',color="w",fontdict = {"fontsize": "xx-large"})

    for i, value in enumerate(most_100_team['100s']):
        ax.text(-value - 0.1, i, str(value), va='center', ha='right', color="w",fontdict = {"fontsize": "xx-large"})
    st.pyplot(fig)
with col2:
    df = most_100_team.merge(most_50_team, on ="Team",)
    st.dataframe(df ,width=300,hide_index=True)


st.subheader("MOST BOUNDARIES")
col1, col2 =st.columns(2)
with col1:
    most_boundaries= utils.team_boundaries(balls)

    fig, ax = plt.subplots()
    fig , ax =utils.plot_look(fig , ax)

    bar_position_team = np.arange(len(most_boundaries))

    ax.barh(bar_position_team, most_boundaries['6s'], label='6',edgecolor="gold")
    ax.barh(bar_position_team, (most_boundaries['4s'] * -1), label='4', color='#FF00A5',edgecolor="gold")


    ax.set_yticks(bar_position_team)
    ax.set_yticklabels(most_boundaries.Team, color="w",fontdict = {"fontsize": "xx-large"})
    ax.set_xticklabels(ax.get_xticks(), color="#320073")
    
    legend = plt.legend(fontsize = "xx-large")
    legend.get_frame().set_facecolor('#320073')
    legend.get_frame().set_edgecolor('white')
    plt.setp(legend.get_texts(), color='w')



    for i, value in enumerate(most_boundaries["6s"]):
        ax.text(value + 0.2, i, str(value), va='center',color="w",fontdict = {"fontsize": "xx-large"})

    for i, value in enumerate(most_boundaries['4s']):
        ax.text(-value - 0.2, i, str(value), va='center', ha='right', color="w",fontdict = {"fontsize": "xx-large"})
    st.pyplot(fig)
with col2:
    df = most_100_team.merge(most_boundaries, on ="Team",)
    st.dataframe(df[["Team","4s","6s"]] ,width=300,hide_index=True)


st.subheader("TEAM WITH MOST WICKETS")
col1, col2 = st.columns(2)
with col1:
    df = utils.team_wickets(balls)
    fig, ax = plt.subplots()
    fig, ax = utils.plot_look(fig, ax)

    plt.bar(df["Team"], df["No. of Wickets"], color =utils.color_scheme(df["No. of Wickets"]), edgecolor="gold")

    ax.set_xticklabels(df.Team, color="w",fontdict = {"fontsize": "xx-large"},rotation =25)
    ax.set_yticklabels(ax.get_xticks(), color="#320073", )

    for i, value in enumerate(df["No. of Wickets"]):
            ax.text(i, int(value)+ 0.2, str(int(value)),
                    ha='center', va='bottom', color="white",fontdict = {"fontsize": "x-large"})

    st.pyplot(fig)
with col2:
    st.dataframe(df, hide_index=True, width =300)





import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import utils


plt.rcParams['figure.facecolor'] = '#320073'
plt.rcParams['axes.facecolor'] = '#320073'
plt.rcParams['xtick.color'] = 'w'
plt.rcParams['ytick.color'] = 'w'
plt.rcParams['text.color'] = 'w'
plt.rcParams['axes.edgecolor'] = 'w'
plt.rcParams['axes.spines.top'] = True
plt.rcParams['axes.spines.bottom'] = True
plt.rcParams['axes.spines.left'] = True
plt.rcParams['axes.spines.right'] = True

st.set_page_config(
    page_title = "Cricket World cup Project - Match Details",
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

st.header("Match Details", divider="gray")

balls = utils.balls
matches = utils.matches 
matches["Unnamed: 0"] = matches['date'] + " , " + matches["team_1"] + ' vs ' + matches["team_2"]
matches['margin']= matches.apply(lambda x : "Wickets" if pd.isnull(x["by_runs"]) else "Runs", axis =1 )

selected_match = st.sidebar.selectbox("Select Match", matches["Unnamed: 0"])

# calculaions
    ## Highest Score innings
higest_score_innings = balls.groupby(["match_id", "batsmen"])[["batsmen_runs"]].sum().sort_values(
            by="batsmen_runs", ascending=False).reset_index()

    ## most Runs
most_runs = balls.groupby(["batsmen"])[["batsmen_runs"]].sum().reset_index(). \
    sort_values(by='batsmen_runs', ascending=False)

    ## most4s
fours_only = balls[balls["batsmen_runs"] == 4]
most_4s = fours_only.groupby(['batsmen'])[['batsmen_runs']].count(). \
    sort_values(by="batsmen_runs", ascending=False).reset_index()

    ## `most 6s`
sixes_only = balls[balls["batsmen_runs"] == 6]
most_6s = sixes_only.groupby(['batsmen'])[['batsmen_runs']].count(). \
    sort_values(by="batsmen_runs", ascending=False).reset_index()

    ## Strike rate in tournament
without_wide = balls[balls['extra_type'] != 'wides']
without_wide_balls = without_wide.groupby(["batsmen"]).agg({"balls": "count", }).\
    rename(columns={"batsmen": "balls_count"})
sr = balls.groupby(["batsmen"]).agg({"batsmen_runs": "sum", }).\
    rename(columns={"batsmen": "balls_count"})
sr = pd.concat([sr, without_wide_balls], axis=1)
sr["strike_rate"] = (sr["batsmen_runs"] / sr['balls']) * 100
sr = sr.reset_index().sort_values(by="strike_rate", ascending=False)

    ## strike rate in innnings
without_wide_inn = balls[balls['extra_type'] != 'wides']
without_wide_balls_inng = without_wide.groupby(["match_id", "batsmen"]).agg({"balls": "count", }). \
    rename(columns={"batsmen": "balls_count"})
sr_inng = balls.groupby(["match_id", "batsmen"]).agg({"batsmen_runs": "sum", }). \
    rename(columns={"batsmen": "balls_count"})
sr_inng = pd.concat([without_wide_balls_inng, sr_inng], axis=1)
sr_inng["strike_rate"] = (sr_inng["batsmen_runs"] / sr_inng['balls']) * 100
sr_inng = sr_inng.sort_values(by="strike_rate", ascending=False).reset_index()


    ## most 50
most_50s = higest_score_innings[
    (higest_score_innings['batsmen_runs'] >= 50) & (higest_score_innings['batsmen_runs'] < 100)]
most_50s = most_50s.groupby(['batsmen']).count().sort_values(by="match_id", ascending=False).reset_index()

    ## most 100
most_100s = higest_score_innings[(higest_score_innings['batsmen_runs'] >= 100)]
most_100s = most_100s.groupby(['batsmen']).count().sort_values(by="match_id", ascending=False).reset_index()

match = matches[matches["Unnamed: 0"] == selected_match]
date = match["date"][match.index[0]]
venue = match["venue"][match.index[0]]
team_match = match["Unnamed: 0"][match.index[0]]
winner = match["match_winner"][match.index[0]]
margin = match["margin"][match.index[0]]
if margin == "Wickets":
    margin_count = match["by_wickets"][match.index[0]].astype("int")
else:
    margin_count = match["by_runs"][match.index[0]].astype("int")
pom = match["player_of_match"][match.index[0]]
match_id = match['match_id'][match.index[0]]
inng_1 = balls[(balls["match_id"] == match['match_id'][match.index[0]]) & (balls["inning_no"] == 1)]
inng_2 = balls[(balls["match_id"] == match['match_id'][match.index[0]]) & (balls["inning_no"] == 2)]
inng1_total_runs = inng_1["total_runs"].sum()
inng2_total_runs = inng_2["total_runs"].sum()
inng1_total_wickets = inng_1["is_wicket"].sum()
inng2_total_wickets = inng_2["is_wicket"].sum()
toss = match["toss_winner"][match.index[0]]
toss_decisiom = match["toss_decision"][match.index[0]]
ump_1 = match["umpire_1"][match.index[0]]
ump_2 = match["umpire_2"][match.index[0]]
tv_ump = match["tv_umpire"][match.index[0]]

not_run_out_1 = inng_1[inng_1["wicket_type"] != "run out"]
bowling_card_1 = not_run_out_1.groupby(["bowler"]).agg({"is_wicket": "sum", "total_runs": "sum"}). \
    reset_index().sort_values(by="is_wicket", ascending=False)
bowling_card_1["bowling_fig"] = bowling_card_1["is_wicket"].astype("str") + "/" + bowling_card_1["total_runs"].astype(
    "str")
bowling_card_1[["bowler", "bowling_fig"]].set_index("bowler")

not_run_out_2 = inng_2[inng_2["wicket_type"] != "run out"]
bowling_card_2 = not_run_out_2.groupby(["bowler"]).agg({"is_wicket": "sum", "total_runs": "sum"}). \
    reset_index().sort_values(by="is_wicket", ascending=False)
bowling_card_2["bowling_fig"] = bowling_card_2["is_wicket"].astype("str") + "/" + bowling_card_2[
    "total_runs"].astype("str")
bowling_card_2[["bowler", "bowling_fig"]].set_index("bowler")

over_by_over_stats_1 = inng_1.groupby("over_num").agg({"total_runs": 'sum', "is_wicket": "sum"}).reset_index()
wickets_scatter_1 = over_by_over_stats_1.apply(lambda x: x['total_runs'] + 1 if x["is_wicket"] != 0 else 0,
                                               axis=1)

over_by_over_stats_2 = inng_2.groupby("over_num").agg({"total_runs": 'sum', "is_wicket": "sum"}).reset_index()
wickets_scatter_2 = over_by_over_stats_2.apply(lambda x: x['total_runs'] + 1 if x["is_wicket"] != 0 else 0,
                                               axis=1)

over_by_over_stats_1["cumsum"] = over_by_over_stats_1["total_runs"].cumsum()
over_by_over_stats_2["cumsum"] = over_by_over_stats_2["total_runs"].cumsum()

worm_scatter_1 = over_by_over_stats_1.apply(lambda x: x["cumsum"] if x["is_wicket"] != 0 else 0, axis=1)
worm_scatter_2 = over_by_over_stats_2.apply(lambda x: x["cumsum"] if x["is_wicket"] != 0 else 0, axis=1)

st.subheader(f'{team_match}')
st.write('Venue :', venue)
st.write(f"{toss} won the toss and choosed to {toss_decisiom}.")
st.subheader(f"{inng_1['batting_team'].unique()[0]} : "
             f"{inng1_total_runs} / {inng1_total_wickets}")
st.subheader(f"{inng_2['batting_team'].unique()[0]} : "
             f"{inng2_total_runs} / {inng2_total_wickets}")
st.subheader(f"{winner} won by {margin_count} {margin} ")
st.markdown(f'Player Of Match : :blue[**{pom}**]')
st.write(f"Match officials : {ump_1} , {ump_2} , {tv_ump}")

st.divider()



st.subheader("Summary", divider="grey")
st.subheader("Batting")
col1, col2 = st.columns(2)
with col1:
    st.write(f'{inng_1["batting_team"].unique()[0]} : '
             f'{inng1_total_runs} / {inng1_total_wickets}')

    st.dataframe(inng_1.groupby(["batsmen"])["batsmen_runs"].sum().reset_index(). \
                 sort_values(by="batsmen_runs", ascending=False).head(3). \
                 rename(columns={"batsmen": f"{inng_1['batting_team'].unique()[0]}",
                                 "batsmen_runs": " "}),

                 width=500, hide_index=True)

with col2:
    st.write(f"{inng_2['batting_team'].unique()[0]} : "
             f"{inng2_total_runs} / {inng2_total_wickets}")
    st.dataframe(inng_2.groupby(["batsmen"])["batsmen_runs"].sum().reset_index(). \
                 sort_values(by="batsmen_runs", ascending=False).head(3). \
                 rename(columns={"batsmen": f"{inng_2['batting_team'].unique()[0]}",
                                 "batsmen_runs": " "}),

                 width=500, hide_index=True)

st.subheader("Bowling")
col1, col2 = st.columns(2)
with col1:
    st.dataframe(bowling_card_1[["bowler", "bowling_fig"]]. \
                 rename(columns={"bowler": f"{inng_2['batting_team'].unique()[0]}",
                                 "bowling_fig": " "}).head(3), width=500, hide_index=True)
with col2:
    st.dataframe(bowling_card_2[["bowler", "bowling_fig"]]. \
                 rename(columns={"bowler": f"{inng_1['batting_team'].unique()[0]}",
                                 "bowling_fig": " "}).head(3), width=500, hide_index=True)

st.divider()
st.subheader("Manhatten", divider="grey")


def mannhatten_wickets_colors(x):
    colors = []

    for value in x:
        if value == 0:
            colors.append("#FF00A5")
        else:
            colors.append("gold")
    return colors


st.write(f"{inng_1['batting_team'].unique()[0]} each over Runs ")
fig, ax = plt.subplots(figsize=(16, 4))

sns.barplot(data=inng_1.groupby('over_num')["total_runs"].sum().reset_index(),
            x=np.arange(inng_1.groupby('over_num')["total_runs"].sum().reset_index().shape[0]),
            y=inng_1.groupby('over_num')["total_runs"].sum().reset_index()["total_runs"],
            color="#FF00A5", edgecolor="gold", width=0.6)

colors = mannhatten_wickets_colors(wickets_scatter_1)
plt.scatter(wickets_scatter_1.index, wickets_scatter_1, marker="s", color=colors)

ax.set_ylabel("Runs", color="w")
ax.set_xlabel("Overs", color="w")
ax.set_xticklabels(ax.get_xticks(), color="w")
ax.set_yticklabels(ax.get_yticks(), color='w')
ax.set_xlim(-1, (inng_1.groupby('over_num')["total_runs"].sum().reset_index().shape[0]))
ax.set_ylim(0, max(ax.get_yticks()) + 1)


st.pyplot(fig)

st.write(f"{inng_2['batting_team'].unique()[0]} each over Runs ")
fig, ax = plt.subplots(figsize=(16, 4))
sns.barplot(data=inng_2.groupby('over_num')["total_runs"].sum().reset_index(),
            x=np.arange(inng_2.groupby('over_num')["total_runs"].sum().reset_index().shape[0]),
            y=inng_2.groupby('over_num')["total_runs"].sum().reset_index()["total_runs"],
            color="#FF00A5", edgecolor="gold", width=0.6)


colors = mannhatten_wickets_colors(wickets_scatter_2)
plt.scatter(wickets_scatter_2.index, wickets_scatter_2, marker="s", color=colors)

ax.set_ylabel("Runs", color="w")
ax.set_xlabel("Overs", color="w")
ax.set_xticklabels(ax.get_xticks(), color="w")
ax.set_yticklabels(ax.get_yticks(), color='w')
ax.set_xlim(-1, (inng_2.groupby('over_num')["total_runs"].sum().reset_index().shape[0]))
ax.set_ylim(0, max(ax.get_yticks()) + 1)


st.pyplot(fig)

st.divider()
st.subheader("Inning Comparision", divider="grey")


def worm_scatter1(x):
    colors = []

    for value in x:
        if value == 0:
            colors.append("#320073")
        else:
            colors.append("#FFD200")
    return colors


def worm_scatter2(x):
    colors = []

    for value in x:
        if value == 0:
            colors.append("#320073")
        else:
            colors.append("#FF00A5")
    return colors


fig, ax = plt.subplots(figsize=(10, 5))
plt.plot(over_by_over_stats_1["cumsum"], color="#D70A0A", label=inng_1["batting_team"].unique()[0])
plt.plot(over_by_over_stats_2["cumsum"], color="#0096D2", label=inng_2["batting_team"].unique()[0])

plt.scatter(over_by_over_stats_1.index, worm_scatter_1, color=worm_scatter1(worm_scatter_1), marker="s")
plt.scatter(over_by_over_stats_2.index, worm_scatter_2, color=worm_scatter2(worm_scatter_2), marker="s")


ax.set_ylabel("Runs", color="w")
ax.set_xlabel("Overs", color="w")
ax.set_xticklabels(ax.get_xticks(), color="w")
ax.set_yticklabels(ax.get_yticks(), color='w')

legend = plt.legend()
legend.get_frame().set_facecolor('#320073')
legend.get_frame().set_edgecolor('white')
plt.setp(legend.get_texts(), color='w')

st.pyplot(fig)
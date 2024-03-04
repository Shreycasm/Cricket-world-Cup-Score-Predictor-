import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import utils as utils

st.set_page_config(
    page_title = "Cricket World cup Project - Player Analysis",
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
selected_player = st.sidebar.selectbox("Select a Player",sorted(utils.all_player_names(balls)))
st.header(f"Player Analysis - {selected_player}", divider="gray")

stats = utils.runs_scored(balls, selected_player)

col1 , col2, col3 , col4 =st.columns(4)
try:
    col1.metric(label = "Total runs",value=stats["batsmen_runs_x"].sum())
except:
    col1.metric(label = "Total runs",value=0)

if stats.shape[0]!= 0:
    col2.metric(label="Highest Score", value=stats["batsmen_runs_x"].max())
else:
    col2.metric(label = "Total runs",value=0)

if stats.shape[0]!= 0:
    col3.metric(label="4s hit", value=stats["4s"].sum())
else:
    col3.metric(label = "Total runs",value=0)

if stats.shape[0] != 0:
    col4.metric(label="6s    hit", value=stats["6s"].sum())
else:
    col4.metric(label = "Total runs",value=0)

if stats.shape[0]!= 0:
    col1.metric(label= "Strike rate",value = np.round(stats["batsmen_runs_x"].sum() /stats["balls"].sum()*100,2))
else:
    col1.metric(label = "Total runs",value=0)

if stats.shape[0]!= 0:
    col2.metric(label="Batting Average",
                value = np.round(stats["batsmen_runs_x"].sum()/ balls[balls["player_out"] == selected_player].shape[0],
                                                          2))
else:
    col2.metric(label = "Total runs",value=0)
total_50 = stats[(stats["batsmen_runs_x"] >= 50)  & (stats["batsmen_runs_x"] < 100)]
total_100 = stats[(stats["batsmen_runs_x"] >= 100)]
try:
    col3.metric(label="50s", value= total_50.shape[0])
except:
    col3.metric(label="50s", value=0)
try:
    col4.metric(label="100s", value= total_100.shape[0])
except:
    col4.metric(label="100s", value=0)

caught = balls[(balls["fielder"] == selected_player) & ((balls["wicket_type"] =="caught") | (balls["wicket_type"] =="caught and bowled"))]
col1.metric(value = caught.shape[0], label ="Catches Took")

run_outs = balls[(balls["fielder"] == selected_player) & (balls["wicket_type"] =="run out")]
col2.metric(label= "Run outs", value = run_outs.shape[0])

stumping = balls[(balls["fielder"] == selected_player) & (balls["wicket_type"] =="stumped")]
col3.metric(label= "Stumping", value = stumping.shape[0])

col4.metric(label=". ", value=" ..")


try:
    wickets = utils.wicket_taken(balls, selected_player)
    col1.metric(label="Wicket Taken", value=wickets[1])
except:
    col1.metric(label="Wicket Taken", value=0)
try:
    maidens = utils.maidens(balls, selected_player)
    col2.metric(label="Maidens", value=maidens)
except:
    col2.metric(label="Maidens", value=0)

try:
    figure = utils.bowling_figure(balls, selected_player)
    col3.metric(label="Best Bowling Figure", value= figure)
except:
    col3.metric(label="Best Bowling Figure", value=0)

try:
    five_wickets = utils.five_wickets(balls, selected_player)
    col4.metric(label="5 Wickets haul", value= five_wickets)
except:
    col4.metric(label="5 Wickets haul", value=0)



st.divider()
st.dataframe(stats.drop(["match_id"], axis=1), width=1500,hide_index=True)
st.divider()


col1, col2 = st.columns(2)
col1.subheader("Runs and Strike rate in each match")
if stats.shape[0] != 0:
    fig, ax = plt.subplots(figsize=(10, 6))


    fig.patch.set_facecolor('#320073')
    ax.set_facecolor('#320073')
    sns.barplot(x = stats.index, y = stats["batsmen_runs_x"],
                palette=utils.color_scheme(stats["batsmen_runs_x"]),
                edgecolor="gold", width=0.8, ci=False,
                )

    plt.plot(stats.index,stats["Strike Rate"],
             linestyle ="--", color= "#D70A0A", marker= "D", label="Strike Rate")

    ax.set_xlabel("Opposition", color="w",fontdict = {"fontsize": "x-large"})
    ax.set_ylabel("Runs", color="w",fontdict = {"fontsize": "x-large"})
    ax.set_xticklabels(stats["bowling_team"], color="w", rotation=25,fontdict = {"fontsize": "x-large"})
    ax.set_yticklabels(ax.get_yticks(), color="w",fontdict = {"fontsize": "x-large"})
    ax.set_xlim(-1, stats.shape[0])
    ax.spines[['top', "bottom", "left", "right"]].set_color('w')
    legend = plt.legend()
    legend.get_frame().set_facecolor('#320073')
    legend.get_frame().set_edgecolor('white')
    plt.setp(legend.get_texts(), color='w')

    for index, value in enumerate(stats["batsmen_runs_x"]):
        plt.text(index, value , str(value), ha='center', va='bottom', color="white",fontdict = {"fontsize": "x-large"})

    col1.pyplot(fig)
else:
    col1.write("DID NOT BAT")

with col2:
    st.subheader("4s vs 6s in each match")
    if stats.shape[0] != 0:

        fig, ax = plt.subplots(figsize=(9, 6))
        fig.patch.set_facecolor('#320073')
        ax.set_facecolor('#320073')
        bar1 = sns.barplot(x=stats.index, y=stats["4s"] +stats["6s"] , edgecolor="gold", ax=ax, label="Count of 4",)

        bar2 = sns.barplot(x=stats.index, y=stats["6s"], color="#FF00A5", ax=ax, label="Count of 6",
                           edgecolor="gold", width=0.8, ci=False)

        ax.set_xlabel("Opposition", color="w",fontdict = {"fontsize": "x-large"})
        ax.set_ylabel("boundary count", color="w",fontdict = {"fontsize": "x-large"})
        ax.set_xticklabels(stats["bowling_team"], color="w", rotation=25,fontdict = {"fontsize": "x-large"})
        yticks = np.arange(0, max(stats["4s"] + stats["6s"]) + 2, 2)
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticks, color="w",fontdict = {"fontsize": "x-large"})
        ax.set_xlim(-1, stats.shape[0])
        ax.set_ylim(0, max(stats["4s"]+stats["6s"])+2)
        ax.spines[['top', "bottom", "left", "right"]].set_color('w')
        legend = plt.legend()
        legend.get_frame().set_facecolor('#320073')
        legend.get_frame().set_edgecolor('white')
        plt.setp(legend.get_texts(), color='w')
        plt.tight_layout()

        st.pyplot(fig)
    else:
        st.write("DID NOT BAT")

##

with col1:
    col1.subheader("% of Runs Scored by type")
    if stats.shape[0] != 0:
        fig , ax = plt.subplots()
        df,_= utils.battting_pie(balls, selected_player)
        plt.pie(df[1:], autopct ="%.2f%%", labels =df[1:].index,
                wedgeprops=dict(edgecolor='gold'),
                textprops={'color': "w"})
        plt.pie(radius = 0.8 , x = [360], colors=['#320073'],
                wedgeprops=dict(edgecolor='gold'))
        fig.patch.set_facecolor('#320073')
        ax.set_facecolor('#320073')

        st.pyplot(fig)
    else:
        st.write("DID NOT BAT")

with col2:
    st.subheader("% of Dotballs ")
    if stats.shape[0] != 0:

        fig , ax = plt.subplots()
        _,df = utils.battting_pie(balls, selected_player=selected_player)
        plt.pie([df[0], df[1:].sum()], autopct ="%.2f%%",labels=["dots balls", "scored balls"],
                colors=['#0096D2', '#FF00A5'],
                wedgeprops=dict(edgecolor='gold'),
                textprops={'color': "w",}
                )
        plt.pie(radius = 0.8 , x = [360], colors=['#320073'],
                wedgeprops=dict(edgecolor='gold'))
        fig.patch.set_facecolor('#320073')
        ax.set_facecolor('#320073')

        st.pyplot(fig)
    else:
        st.write("DID NOT BAT")

with col1:
    col1.subheader("Dismissial Kind")
    if stats.shape[0] != 0:
        fig , ax = plt.subplots()
        df= utils.dismissial_kind(balls, selected_player)
        plt.pie(df[1:], autopct ="%.2f%%", labels =df[1:].index,
                wedgeprops=dict(edgecolor='gold'),
                textprops={'color': "w"})
        plt.pie(radius = 0.8 , x = [360], colors=['#320073'],
                wedgeprops=dict(edgecolor='gold'))
        fig.patch.set_facecolor('#320073')
        ax.set_facecolor('#320073')

        st.pyplot(fig)
    else:
        st.write("DID NOT BAT")
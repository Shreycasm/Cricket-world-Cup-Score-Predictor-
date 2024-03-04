import pandas as pd
import numpy as np
import pickle
import gzip


balls = pd.read_csv("./artifacts/cwc2023_balls.csv")
matches = pd.read_csv("./artifacts/cwc_2023_matches.csv")
matches["Unnamed: 0"] = matches['date'] + " , " + matches["team_1"] + ' vs ' + matches["team_2"]

with gzip.open("./artifacts/model.pkl", 'rb') as file:
            model = pickle.load(file)  



# PLOTTING
## BARS COLOR
def color_scheme(value_counts):
    colors = []
    for i in value_counts:
        if i == value_counts.max():
            colors.append('#0096D2')
        else:
            colors.append('#FF00A5')

    return colors

### PLOT LOOK
def plot_look(fig, ax):
    fig.patch.set_facecolor('#320073')
    ax.set_facecolor('#320073')

    ax.spines['top'].set_color('w')
    ax.spines['bottom'].set_color('w')
    ax.spines['left'].set_color('w')
    ax.spines['right'].set_color('w')

    return fig, ax


########################################################################################################################################################################

# OVERALL STATS
## MOST MATCHES WON
def mot_matches_won(matches_df):
    return matches_df["match_winner"].value_counts().reset_index().rename(columns= {"match_winner":"Team", "count":"No of Wins"})


## MOST TOSS WON
def most_toss_won(matches_df):
    return matches_df["toss_winner"].value_counts().reset_index().rename(columns= {"toss_winner":"Team", "count":"No of Wins"})


## TOSS DECISION
def toss_decision(matches_df):
    return matches_df["toss_decision"].value_counts().reset_index()


## TOSS WIN MATCH WIN
def toss_win_match_win(matches_df):
    return np.round(matches_df[matches_df["toss_winner"] == matches_df["match_winner"]].shape[0]/ matches_df.shape[0]*100)


## TOSS DECISION BY VENUE
def toss_decision_by_venue(matches_df):
    return matches_df.groupby(["city", "toss_decision"]).size().unstack().reset_index().rename(columns={"city":"City", "bat":"Bat", "field":"Field"}).fillna(0)


## AVERAGE 1st Inngings SCORE AT DIFFERENT VENUE
def average_score_venue(matches_df, balls_df):
    venue = balls_df.merge(matches_df[["match_id", "city"]], on ="match_id" )
    first_inn = venue[venue["inning_no"] == 1]
    df = np.round(first_inn.groupby(["city"])["total_runs"].sum() / matches_df["city"].value_counts().sort_index()).reset_index().\
        rename(columns={"city":"City", "bat":"Bat", 0:"Avg. Score"})
    return df


## TEAM WITH MOST 50+
each_match_50_up= balls.groupby(["match_id", "batting_team", "batsmen"])["batsmen_runs"].sum().reset_index()
def most_100_n_50_team(balls_df):
        most_100s_team = each_match_50_up[each_match_50_up["batsmen_runs"] > 99].groupby('batting_team')["batsmen_runs"].count().reset_index()
        most_100s_team.loc[len(most_100s_team)] = {"batting_team":"Netherlands","batsmen_runs":0}
        most_100s_team = most_100s_team.sort_values(by="batting_team").rename(columns = {'batting_team':'Team', "batsmen_runs":"100s"})


        most_50_team = each_match_50_up[(each_match_50_up["batsmen_runs"] > 49) & (each_match_50_up["batsmen_runs"] <= 99) ].\
            groupby('batting_team')["batsmen_runs"].count().reset_index().sort_values(by="batting_team").rename(columns = {'batting_team':'Team', "batsmen_runs":"50s"})

        return most_100s_team, most_50_team


## EACH TEAMS BOUNDARIES
def team_boundaries(balls_df):
    fours_balls = balls_df[balls_df["batsmen_runs"] == 4]
    total_fours_team = fours_balls.groupby("batting_team")["batsmen_runs"].count().reset_index()

    sixes_balls = balls_df[balls_df["batsmen_runs"] == 6]
    total_sixes_team = sixes_balls.groupby("batting_team")["batsmen_runs"].count().reset_index()

    total_boundaries = total_sixes_team.merge(total_fours_team, on ="batting_team").rename(columns={"batting_team":"Team", "batsmen_runs_x":"6s", "batsmen_runs_y":'4s'})

    return total_boundaries


## Most_wins
def most_wins(matches_df):
    most_wins = matches_df["match_winner"].value_counts()
   
   

##########################################################################################################################################################################



# BATTING  STATS 
## HIGHEST SCORE IN AN INNING
def highest_score(balls_df,selected_team="All"):
    if selected_team == "All":
        df = balls_df.groupby(["match_id", "batsmen"])[["batsmen_runs"]].sum().sort_values(by="batsmen_runs",
                                                                            ascending=False).reset_index()
    else:
        df = balls_df[balls_df["batting_team"] == selected_team]
        df = df.groupby(["match_id", "batsmen"])[["batsmen_runs"]].sum().sort_values(by="batsmen_runs",
                                                                            ascending=False).reset_index()
    return df


## MOST RUNS IN TOURNAMENT
def most_runs(balls_df, selected_team="All"):
    if selected_team == "All":
        df = balls_df.groupby(["batsmen"])[["batsmen_runs"]].sum().reset_index().\
            sort_values(by='batsmen_runs', ascending=False)
    else:
        df = balls_df[balls_df["batting_team"] == selected_team]
        df = df.groupby(["batsmen"])[["batsmen_runs"]].sum().reset_index(). \
            sort_values(by='batsmen_runs', ascending=False)
    return df


## MOST 4s IN TOURNAMENT 
def most_4s(balls_df, selected_team="All"):
    if selected_team == "All":
        fours_only = balls_df[balls_df["batsmen_runs"] == 4]
        df = fours_only.groupby(['batsmen'])[['batsmen_runs']].count(). \
            sort_values(by="batsmen_runs", ascending=False).reset_index()
    else:
        df = balls_df[balls_df["batting_team"] == selected_team]
        fours_only1 = df[df["batsmen_runs"] == 4]
        df = fours_only1.groupby(['batsmen'])[['batsmen_runs']].count(). \
            sort_values(by="batsmen_runs", ascending=False).reset_index()
    return  df


## MOST 6s IN TOURNAMENT 
def most_6s(balls_df, selected_team="All"):
    if selected_team == "All":
        sixes_only = balls_df[balls_df["batsmen_runs"] == 6]
        df = sixes_only.groupby(['batsmen'])[['batsmen_runs']].count(). \
            sort_values(by="batsmen_runs", ascending=False).reset_index()
    else:
        df = balls_df[balls_df["batting_team"] == selected_team]
        sixes_only = df[df["batsmen_runs"] == 6]
        df = sixes_only.groupby(['batsmen'])[['batsmen_runs']].count(). \
            sort_values(by="batsmen_runs", ascending=False).reset_index()
    return  df


## BEST BATTING STRIKE RATE IN TOURNAMENT
def sr(balls_df, selected_team="All"):
    if selected_team == "All":
        without_wide = balls_df[balls_df['extra_type'] != 'wides']
        without_wide_balls = without_wide.groupby(["batsmen"]).agg({"balls": "count", }).\
            rename(columns={"batsmen": "balls_count"})
        df = balls_df.groupby(["batsmen"]).agg({"batsmen_runs": "sum", }). \
            rename(columns={"batsmen": "balls_count"})
        df = pd.concat([df, without_wide_balls], axis=1)
        df["strike_rate"] = (df["batsmen_runs"] / df['balls']) * 100
        df = df.reset_index().sort_values(by="strike_rate", ascending=False)
    else:
        df = balls_df[balls_df["batting_team"] == selected_team]
        without_wide1 = df[df['extra_type'] != 'wides']
        without_wide_balls1 = without_wide1.groupby(["batsmen"]).agg({"balls": "count", }). \
            rename(columns={"batsmen": "balls_count"})
        df = df.groupby(["batsmen"]).agg({"batsmen_runs": "sum", }). \
            rename(columns={"batsmen": "balls_count"})
        df = pd.concat([df, without_wide_balls1], axis=1)
        df["strike_rate"] = (df["batsmen_runs"] / df['balls']) * 100
        df = df.reset_index().sort_values(by="strike_rate", ascending=False)

    return df


## BEST BATTING STRIKE RATE IN AN INNING
def sr_inng(balls_df, selected_team="All"):
    if selected_team == "All":
        without_wide_inn = balls_df[balls_df['extra_type'] != 'wides']
        without_wide_balls_inng = without_wide_inn.groupby(["match_id", "batsmen"]).agg({"balls": "count", }). \
            rename(columns={"batsmen": "balls_count"})
        df = balls.groupby(["match_id", "batsmen"]).agg({"batsmen_runs": "sum", }). \
            rename(columns={"batsmen": "balls_count"})
        df = pd.concat([without_wide_balls_inng, df], axis=1)
        df["strike_rate"] = (df["batsmen_runs"] / df['balls']) * 100
        df = df.sort_values(by="strike_rate", ascending=False).reset_index()
    else:
        df = balls_df[balls_df["batting_team"] == selected_team]
        without_wide_inn1 = df[df['extra_type'] != 'wides']
        without_wide_balls_inng1 = without_wide_inn1.groupby(["match_id", "batsmen"]).agg({"balls": "count", }). \
            rename(columns={"batsmen": "balls_count"})
        df = df.groupby(["match_id", "batsmen"]).agg({"batsmen_runs": "sum", }). \
            rename(columns={"batsmen": "balls_count"})
        df = pd.concat([without_wide_balls_inng1, df], axis=1)
        df["strike_rate"] = (df["batsmen_runs"] / df['balls']) * 100
        df = df.sort_values(by="strike_rate", ascending=False).reset_index()

    return df


## BEST BATTING STRIKE RATE IN AVERAGE
def average(balls_df, selected_team="All"):

    df = most_runs(balls_df, selected_team)
    df1 = balls_df[balls_df["wicket_type"] != "retired hurt"]
    df1 = df1.groupby(["player_out"])[["player_out"]].count().rename({"player_out": "out_num"},
                       axis=1).reset_index().rename({"player_out": "batsmen"}, axis=1)
    df = df.merge(df1, on="batsmen", how="outer")
    df["avg"] = np.round(df["batsmen_runs"] / df["out_num"],2)

    return df.sort_values(by="avg", ascending=False)


##MOST 50s IN THE TOURNAMENT
def most_50s(balls_df, selected_team="All"):
    if selected_team == "All":
        higest_score_innings = highest_score(balls_df, selected_team="All")
        df = higest_score_innings[
            (higest_score_innings['batsmen_runs'] >= 50) & (higest_score_innings['batsmen_runs'] < 100)]
        df = df.groupby(['batsmen']).count().sort_values(by="match_id", ascending=False).reset_index()
    else:
        df = balls[balls["batting_team"] == selected_team]
        df1 = df.groupby(["match_id", "batsmen"])[["batsmen_runs"]].sum().sort_values(
            by="batsmen_runs", ascending=False).reset_index()
        df = df1[(df1['batsmen_runs'] >= 50) & (df1['batsmen_runs'] < 100)]
        df = df.groupby(['batsmen']).count().sort_values(by="match_id", ascending=False).reset_index()

    return df


##MOST 100s IN THE TOURNAMENT
def most_100s(balls_df, selected_team="All"):

    if selected_team == "All":
        higest_score_innings = highest_score(balls_df, selected_team="All")
        df = higest_score_innings[
            (higest_score_innings['batsmen_runs'] >= 100)]
        df = df.groupby(['batsmen']).count().sort_values(by="match_id", ascending=False).reset_index()
    else:
        df = balls[balls["batting_team"] == selected_team]
        df1 = df.groupby(["match_id", "batsmen"])[["batsmen_runs"]].sum().sort_values(
            by="batsmen_runs", ascending=False).reset_index()
        df = df1[(df1['batsmen_runs'] >= 100)]
        df = df.groupby(['batsmen']).count().sort_values(by="match_id", ascending=False).reset_index()

    return df



##########################################################################################################################################################################



# PLAYER ANALYSIS
## ALL PLAYER NAMES
def all_player_names(balls_df):
    player =  balls_df["batsmen"].unique().tolist() + balls_df["bowler"].unique().tolist()
    player = set(player)

    return player


## RUNS SCORED BY PLAYER
def runs_scored(balls_df , selected_player =None):
    selected_player_balls = balls_df[balls_df["batsmen"] == selected_player]
    stats = selected_player_balls[selected_player_balls["extra_type"] != 'wides'].groupby(["match_id","bowling_team"]).\
            agg({"batsmen_runs":"sum", "balls":"count"}).reset_index()
    stats["Strike Rate"] = np.round((stats["batsmen_runs"] / stats["balls"]) * 100, 2)
    fours = selected_player_balls[selected_player_balls["batsmen_runs"] == 4].copy()
    fours["batsmen_runs"] = fours["batsmen_runs"].astype("int")
    sixes = selected_player_balls[selected_player_balls["batsmen_runs"] == 6].copy()
    sixes["batsmen_runs"] = sixes["batsmen_runs"].astype("int")


    stats = stats.merge(fours.groupby(["match_id"])["batsmen_runs"].count(), on="match_id", how="left").rename(
        columns={"batsmen_runs_y": "4s"})
    stats = stats.merge(sixes.groupby(["match_id"])["batsmen_runs"].count(), on="match_id", how="left").rename(
        columns={"batsmen_runs": "6s"})

    stats = stats.fillna(0)
    stats["4s"] = stats["4s"].astype("int")
    stats["6s"] = stats["6s"].astype("int")

    stats.rename({"batsmen_runs_x":'Batsmen', 'balls':"Balls Played", "bowling_taem" :"Bowling Team"})


    return stats


## RUN TYPE DISTRIBUTION
def battting_pie(ball_df, selected_player =None):
    selected_player_balls = ball_df[ball_df["batsmen"] == selected_player]
    run_dist = selected_player_balls.groupby(["batsmen_runs"])["batsmen_runs"].sum()
    dot_ball_per = selected_player_balls.groupby(["batsmen_runs"])["batsmen_runs"].count()
    return run_dist , dot_ball_per


## DISMISSIAL KIND OF PLAYER WHILE BATTING
def dismissial_kind(ball_df, selected_player =None):
    selected_player_balls = ball_df[ball_df["batsmen"] == selected_player]
    dismissial_kind = selected_player_balls["wicket_type"].value_counts()
    return dismissial_kind


## WICKETS TAKEN BY PLAYER
def wicket_taken(ball_df, selected_player =None):
    selected_player_balls = ball_df[ball_df["bowler"] == selected_player]
    wickets = selected_player_balls[(selected_player_balls["wicket_type"] != "run out") &
                              (selected_player_balls["wicket_type"] != "retired hut")]["is_wicket"].value_counts().\
        sort_values()
    return wickets


## MAIDEN BOWLED BY PLAYER
def maidens(balls_df , selected_player=None):
    selected_player_balls = balls_df[balls_df["bowler"] == selected_player]
    without_byes = selected_player_balls[(selected_player_balls["extra_type"] != "byes") & (selected_player_balls["extra_type"] != "legbyes")]
    maidens = without_byes.groupby(["match_id", "over_num"])["total_runs"].sum().reset_index()
    maidens = maidens[maidens["total_runs"] == 0].shape[0]
    return maidens


## BEST BOWLING FIGURE OF PLAYER
def bowling_figure(ball_df, selected_player=None):
    selected_player_balls = ball_df[ball_df["bowler"] == selected_player]
    without_byes = selected_player_balls[(selected_player_balls["extra_type"] != "byes") &
                                         (selected_player_balls["extra_type"] != "legbyes")]
    figure = without_byes[(without_byes["wicket_type"] != "retired hurt") & (without_byes["wicket_type"] != "run out")]. \
        groupby(["match_id"]).agg({"total_runs": "sum", "is_wicket": "sum"}). \
        sort_values(by=['is_wicket', "total_runs"], ascending=[False, True])

    return f'{figure["total_runs"].iloc[0]}/{figure["is_wicket"].iloc[0]}'


## 5 WICKETS HAUL BY PLAYER
def five_wickets(ball_df, selected_player=None):
    selected_player_balls = ball_df[ball_df["bowler"] == selected_player]
    without_byes = selected_player_balls[(selected_player_balls["extra_type"] != "byes") &
                                         (selected_player_balls["extra_type"] != "legbyes")]
    figure = without_byes[(without_byes["wicket_type"] != "retired hurt") & (without_byes["wicket_type"] != "run out")]. \
        groupby(["match_id"]).agg({"total_runs": "sum", "is_wicket": "sum"}). \
        sort_values(by=['is_wicket', "total_runs"], ascending=[False, True])
    return figure[figure['is_wicket'] >= 5].shape[0]




import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

pd.options.display.max_rows = 60 

df = pd.read_csv('datasets/matches.csv')

df["goals_scored"] = df["home_team_score"] + df["away_team_score"] 

df["goals_diff"] = df["home_team_score"] - df["away_team_score"]

df["friendly_score"] = df["home_team_score"].map(str) + 'x' + df["away_team_score"].map(str)

final_result = []
points_home_team = []
points_away_team = []

win_home_team = []
loss_home_team = []
tie_home_team = []

win_away_team = []
loss_away_team = []
tie_away_team = []

for row in df["goals_diff"]:
    if row == 0:
        final_result.append("TIE")
        win_home_team.append(0)
        loss_home_team.append(0)
        tie_home_team.append(1)
        win_away_team.append(0)
        loss_away_team.append(0)
        tie_away_team.append(1)
    if row > 0:
        final_result.append("HOME WINNER")
        win_home_team.append(1)
        loss_home_team.append(0)
        tie_home_team.append(0)
        win_away_team.append(0)
        loss_away_team.append(1)
        tie_away_team.append(0) 
    if row < 0:
        final_result.append("AWAY WINNER")           
        win_home_team.append(0)
        loss_home_team.append(1)
        tie_home_team.append(0)
        win_away_team.append(1)
        loss_away_team.append(0)
        tie_away_team.append(0)

df["final_result"] = final_result

df["win_home_team"] = win_home_team
df["loss_home_team"] = loss_home_team
df["tie_home_team"] = tie_home_team

df["win_away_team"] = win_away_team
df["loss_away_team"] = loss_away_team
df["tie_away_team"] = tie_away_team

# Somatórios e Médias

total_goals = df["goals_scored"].sum()

matches = df.__len__()

avg_goals_by_game = df["goals_scored"].mean()

standings_home = df.groupby(['championship', 'home_team']).aggregate(
    {'round': 'count', 'win_home_team': 'sum', 'tie_home_team': 'sum',
     'loss_home_team': 'sum', 'home_team_score': 'sum', 'away_team_score': 'sum'})

standings_away = df.groupby(['championship', 'away_team']).aggregate(
    {'round': 'count', 'win_away_team': 'sum', 'tie_away_team': 'sum', 
     'loss_away_team': 'sum', 'away_team_score': 'sum', 'home_team_score': 'sum'})

standings = standings_home.reset_index().merge(standings_away, how='left', left_on=['home_team','championship'], 
                                 right_on=['away_team','championship']).set_index(['championship'])

standings.rename(columns={'home_team': 'team', 'round_x': 'matches_played_home', 'win_home_team':'wins_home',
                          'loss_home_team':'losses_home', 'tie_home_team':'ties_home', 'home_team_score_x':'goals_scored_home',
                          'away_team_score_x':'goals_conceded_home', 'round_y': 'matches_played_away', 'win_away_team':'wins_away',
                          'loss_away_team':'losses_away', 'tie_away_team':'ties_away', 'away_team_score_y':'goals_scored_away',
                          'home_team_score_y':'goals_conceded_away'}, inplace=True)
                                 
standings["matches_played"] = standings["matches_played_home"] + standings["matches_played_away"]

standings["wins"] = standings["wins_home"] + standings["wins_away"]
standings["ties"] = standings["ties_home"] + standings["ties_away"]
standings["losses"] = standings["losses_home"] + standings["losses_away"]

standings["points_home"] = 3 * standings["wins_home"] + standings["ties_home"]
standings["points_away"] = 3 * standings["wins_away"] + standings["ties_away"]
standings["points"] = 3 * standings["wins"] + standings["ties"]

standings["goals_scored"] = standings["goals_scored_home"] + standings["goals_scored_away"]
standings["goals_conceded"] = standings["goals_conceded_home"] + standings["goals_conceded_away"]

standings["goals_diff_home"] = standings["goals_scored_home"] - standings["goals_conceded_home"]
standings["goals_diff_away"] = standings["goals_scored_away"] - standings["goals_conceded_away"]
standings["goals_diff"] = standings["goals_scored"] - standings["goals_conceded"]

standings["points_percent_home"] = standings["points_home"] / (3 * standings["matches_played_home"])
standings["points_percent_away"] = standings["points_away"] / (3 * standings["matches_played_away"])
standings["points_percent"] = standings["points"] / (3 * standings["matches_played"])

standings.sort_values(['championship', 'points', 'wins', 'goals_diff', 'goals_scored'],
                       ascending=[True, False, False, False, False], inplace=True)

championship_metrics = df.groupby(['championship']).aggregate(
    {'round': 'count', 'win_home_team': 'sum', 'tie_home_team': 'sum',
     'loss_home_team': 'sum', 'home_team_score': ['sum', 'mean'], 'away_team_score': ['sum', 'mean']})

filepath = Path('out/classificacao.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)  
standings.to_csv(filepath)

filepath = Path('out/metricas_campeonato.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)  
championship_metrics.to_csv(filepath)
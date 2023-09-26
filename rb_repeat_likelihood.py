# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 23:08:28 2023
Calculate Likelihood of RB2 season given RB Finish
@author: Jan Calalo
"""



import nfl_data_py as nfl
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import scipy.optimize as opti
import pandas as pd
import matplotlib.pyplot as plt

#%%

playernfl = nfl.import_players()

#%%
relevant_years = np.arange(2010,2023).tolist()
relevant_data = ['player_id','position','receptions','targets','rushing_yards','receiving_yards',
                 'passing_yards','season_type','season','week','receiving_tds','rushing_attempts']
# player_catches_targets = nfl.import_weekly_data(relevant_years)#, columns = relevant_data)

test_out = nfl.import_seasonal_data(relevant_years,s_type = 'REG')


#%%

test_out['POS'] = np.nan
seasonal_data_w_pos = test_out
unique_player_ids = seasonal_data_w_pos['player_id'].unique()
#%% sorting player positions in outcomes
player_names = []
pos_out = []
for x in range(len(test_out)):
    player_names.append(playernfl[playernfl['gsis_id'] == test_out['player_id'][x]]['display_name'].values[0])
    pos_out.append(playernfl[playernfl['gsis_id'] == test_out['player_id'][x]]['position'].values[0])
    

test_out['Player_Names'] = player_names
test_out['Positions'] = pos_out
#%%

rb_season_data = test_out[test_out['Positions'] == 'RB'][['player_id','season','Positions','Player_Names','fantasy_points_ppr','fantasy_points']]
rb_season_data['Season_Finish'] = np.nan
rb_season_data = rb_season_data.reset_index()
#%%
x = 0
curr_year = relevant_years[x]

for curr_year in relevant_years:
    # curr_rb_seasons = rb_season_data.query('season == curr_year')
    curr_rb_seasons = rb_season_data[rb_season_data['season']  == curr_year]
    
    sorted_curr_rb_season = curr_rb_seasons.sort_values('fantasy_points',ascending = False).reset_index()
    # seasonal_rankings 
    
    for y in range(len(sorted_curr_rb_season)):
        curr_index = sorted_curr_rb_season['level_0'][y]
        rb_season_data['Season_Finish'][curr_index] = y+1


#%%

top_20rbs = rb_season_data[rb_season_data['Season_Finish'] <= 20].reset_index()

len_data = len(top_20rbs[top_20rbs['season']<= 2021])

#%% repeat 1 season fantasy finish

number_repeats = np.zeros(20)
for m in range(1,21):
    for p in np.arange(2010,2022).tolist():
        curr_player_id = top_20rbs[(top_20rbs["Season_Finish"] == m) & (top_20rbs["season"] == p)]["player_id"].values[0]
        
        
        if curr_player_id in top_20rbs[top_20rbs["season"] == p+1]['player_id'].values:
            number_repeats[m-1] += 1
        else:
            _ = 0
            


#%%

curr_fig = plt.figure()
curr_ax = curr_fig.add_axes([.15,.15,.8,.8])
curr_ax.bar(np.arange(1,21),number_repeats/12 * 100)
curr_ax.set_xticks([1,5,10,15,20])
curr_ax.set_yticks(np.arange(0,101,20))
curr_ax.set_ylim(0,100)
curr_ax.spines['top'].set_visible(False)

curr_ax.spines['right'].set_visible(False)

curr_ax.set_xlabel('Season Fantasy Finish (Rank)')
curr_ax.set_title('Likelihood RB Repeating a Top 20 Finish ')

curr_ax.set_ylabel('Likelihood\nTop 20 RB finish(%)')

#%%

number_repeats = np.zeros(20)
for m in range(1,21):
    for p in np.arange(2010,2021).tolist():
        curr_player_id = top_20rbs[(top_20rbs["Season_Finish"] == m) & (top_20rbs["season"] == p)]["player_id"].values[0]
        
        
        if curr_player_id in top_20rbs[top_20rbs["season"] == p+1]['player_id'].values:
            if curr_player_id in top_20rbs[top_20rbs["season"] == p+2]['player_id'].values:
                number_repeats[m-1] += 1
        else:
            _ = 0
            


#%%

curr_fig = plt.figure()
curr_ax = curr_fig.add_axes([.15,.15,.8,.8])
curr_ax.bar(np.arange(1,21),number_repeats/12 * 100)
curr_ax.set_xticks([1,5,10,15,20])
curr_ax.set_yticks(np.arange(0,101,20))
curr_ax.set_ylim(0,100)
curr_ax.spines['top'].set_visible(False)

curr_ax.spines['right'].set_visible(False)

curr_ax.set_xlabel('Season Fantasy Finish (Rank)')
curr_ax.set_title('Likelihood RB Repeating a Top 20\nFinish in both the next 2 seasons',y =1 ,pad = -15)

curr_ax.set_ylabel('Likelihood\nTop 20 RB finish (%)')

#%%

number_repeats = np.zeros(20)
for m in range(1,21):
    for p in np.arange(2010,2020).tolist():
        curr_player_id = top_20rbs[(top_20rbs["Season_Finish"] == m) & (top_20rbs["season"] == p)]["player_id"].values[0]
        
        
        if curr_player_id in top_20rbs[top_20rbs["season"] == p+1]['player_id'].values:
            number_repeats[m-1] += 1
        elif curr_player_id in top_20rbs[top_20rbs["season"] == p+2]['player_id'].values:
            number_repeats[m-1] += 1
        elif curr_player_id in top_20rbs[top_20rbs["season"] == p+3]['player_id'].values:
            number_repeats[m-1] += 1
        else:
            _ = 0
            


#%%

curr_fig = plt.figure()
curr_ax = curr_fig.add_axes([.15,.15,.8,.8])
curr_ax.bar(np.arange(1,21),number_repeats/12 * 100)
curr_ax.set_xticks([1,5,10,15,20])
curr_ax.set_yticks(np.arange(0,101,20))
curr_ax.set_ylim(0,100)
curr_ax.spines['top'].set_visible(False)

curr_ax.spines['right'].set_visible(False)

curr_ax.set_xlabel('Season Fantasy Finish (Rank)')
curr_ax.set_title('Likelihood RB Repeating a Top 20\nFinish in at least one of the next 2 seasons',y =1 ,pad = -15)

curr_ax.set_ylabel('Likelihood\nTop 20 RB finish (%)')
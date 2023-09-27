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
#%% load all players

playernfl = nfl.import_players()

#%%
#%% load relevant years
relevant_years = np.arange(2010,2023).tolist()
relevant_data = ['player_id','position','receptions','targets','rushing_yards','receiving_yards',
                 'passing_yards','season_type','season','week','receiving_tds','rushing_attempts']
# player_catches_targets = nfl.import_weekly_data(relevant_years)#, columns = relevant_data)

allplayer_seasonal = nfl.import_seasonal_data(relevant_years,s_type = 'REG')


#%%
#%% generate positional list from seasonal finishes

#%% sorting player positions in outcomes
player_names = []
pos_out = []
for x in range(len(allplayer_seasonal)):
    player_names.append(playernfl[playernfl['gsis_id'] == allplayer_seasonal['player_id'][x]]['display_name'].values[0])
    pos_out.append(playernfl[playernfl['gsis_id'] == allplayer_seasonal['player_id'][x]]['position'].values[0])
    

<<<<<<< HEAD
allplayer_seasonal['Player_Names'] = player_names
allplayer_seasonal['Positions'] = pos_out
#%%
=======
test_out['Player_Names'] = player_names
test_out['Positions'] = pos_out
#%% Generating list for just rbs
>>>>>>> a3a6f67a4b1dd0cfb10ee87cfc5c8a17f3358f59

rb_season_data = allplayer_seasonal[allplayer_seasonal['Positions'] == 'RB'][['player_id','games','season','Positions','Player_Names','fantasy_points_ppr','fantasy_points']]
rb_season_data['Season_Finish'] = np.nan
rb_season_data = rb_season_data.reset_index()

rb_season_data['FPG'] = rb_season_data['fantasy_points']/rb_season_data['games']

#%%
x = 0
curr_year = relevant_years[x]

for curr_year in relevant_years:
    # curr_rb_seasons = rb_season_data.query('season == curr_year')
    curr_rb_seasons = rb_season_data[rb_season_data['season']  == curr_year]
    
    sorted_curr_rb_season = curr_rb_seasons.sort_values('FPG',ascending = False).reset_index()
    # seasonal_rankings 
    
    for y in range(len(sorted_curr_rb_season)):
        curr_index = sorted_curr_rb_season['level_0'][y]
        rb_season_data['Season_Finish'][curr_index] = y+1


#%%
great_thresh = 10

top_20rbs = rb_season_data[rb_season_data['Season_Finish'] <= great_thresh].reset_index()

len_data = len(top_20rbs[top_20rbs['season']<= 2021])

#%% repeat 1 season fantasy finish

number_repeats = np.zeros(great_thresh)
for m in range(1,great_thresh+1):
    for p in np.arange(2010,2022).tolist():
        curr_player_id = top_20rbs[(top_20rbs["Season_Finish"] == m) & (top_20rbs["season"] == p)]["player_id"].values[0]
        
        
        if curr_player_id in top_20rbs[top_20rbs["season"] == p+1]['player_id'].values:
            number_repeats[m-1] += 1
        else:
            _ = 0
            


#%%

curr_fig = plt.figure()
curr_ax = curr_fig.add_axes([.15,.15,.8,.8])
curr_ax.bar(np.arange(1,great_thresh+1),number_repeats/12 * 100)
curr_ax.set_xticks(np.linspace(1,great_thresh,great_thresh))
curr_ax.set_yticks(np.arange(0,101,20))
curr_ax.set_ylim(0,100)
curr_ax.spines['top'].set_visible(False)

curr_ax.spines['right'].set_visible(False)

curr_ax.set_xlabel('Season Fantasy Finish (Rank)')
curr_ax.set_title(f'Likelihood RB Repeating a Top {great_thresh} Finish ')

curr_ax.set_ylabel(f'Likelihood\nTop {great_thresh} RB finish(%)')


number_repeats = np.zeros(great_thresh)
for m in range(1,great_thresh+1):
    for p in np.arange(2010,2021).tolist():
        curr_player_id = top_20rbs[(top_20rbs["Season_Finish"] == m) & (top_20rbs["season"] == p)]["player_id"].values[0]
        
        
        if curr_player_id in top_20rbs[top_20rbs["season"] == p+1]['player_id'].values:
            if curr_player_id in top_20rbs[top_20rbs["season"] == p+2]['player_id'].values:
                number_repeats[m-1] += 1
        else:
            _ = 0
            


#%%% plot 2 repeat seasons after top 20 finish

curr_fig = plt.figure()
curr_ax = curr_fig.add_axes([.15,.15,.8,.8])
curr_ax.bar(np.arange(1,great_thresh+1),number_repeats/11 * 100)
curr_ax.set_xticks(np.linspace(1,great_thresh,great_thresh))
curr_ax.set_yticks(np.arange(0,101,20))
curr_ax.set_ylim(0,100)
curr_ax.spines['top'].set_visible(False)

curr_ax.spines['right'].set_visible(False)

curr_ax.set_xlabel('Season Fantasy Finish (Rank)')
curr_ax.set_title(f'Likelihood RB Repeating a Top {great_thresh}\nFinish in both the next 2 seasons',y =1 ,pad = -15)

curr_ax.set_ylabel(f'Likelihood\nTop {great_thresh} RB finish (%)')

#%% calculate either of 2 fololowing seasons after top 20 finish

number_repeats = np.zeros(great_thresh)
for m in range(1,great_thresh+1):
    for p in np.arange(2010,2021).tolist():
        curr_player_id = top_20rbs[(top_20rbs["Season_Finish"] == m) & (top_20rbs["season"] == p)]["player_id"].values[0]
        
        
        if curr_player_id in top_20rbs[top_20rbs["season"] == p+1]['player_id'].values:
            number_repeats[m-1] += 1
        elif curr_player_id in top_20rbs[top_20rbs["season"] == p+2]['player_id'].values:
            number_repeats[m-1] += 1
        # elif curr_player_id in top_20rbs[top_20rbs["season"] == p+3]['player_id'].values:
        #     number_repeats[m-1] += 1
        else:
            _ = 0
            


#%%% plot either of 2 fololowing seasons after top 20 finish

curr_fig = plt.figure()
curr_ax = curr_fig.add_axes([.15,.15,.8,.8])
curr_ax.bar(np.arange(1,great_thresh+1),number_repeats/11 * 100)
curr_ax.set_xticks(np.linspace(1,great_thresh,great_thresh))
curr_ax.set_yticks(np.arange(0,101,20))
curr_ax.set_ylim(0,100)
curr_ax.spines['top'].set_visible(False)

curr_ax.spines['right'].set_visible(False)

curr_ax.set_xlabel('Season Fantasy Finish (Rank)')
curr_ax.set_title(f'Likelihood RB Repeating a Top {great_thresh}\nFinish in at least one of the next 2 seasons',y =1 ,pad = -15)

<<<<<<< HEAD
curr_ax.set_ylabel(f'Likelihood\nTop {great_thresh} RB finish (%)')
=======
curr_ax.set_ylabel('Likelihood\nTop 20 RB finish (%)')
>>>>>>> a3a6f67a4b1dd0cfb10ee87cfc5c8a17f3358f59

# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 18:47:39 2023
predictive power of week x to final fantasy standings
@author: Jan Calalo
"""



import nfl_data_py as nfl
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import scipy.optimize as opti
import pandas as pd
import matplotlib.pyplot as plt


import fantasyfootball_functions as fff
#%%
playernfl = nfl.import_players()

relevant_years = np.arange(2010,2023).tolist()
relevant_data = ['player_id','position','receptions','targets','rushing_yards','receiving_yards',
                 'passing_yards','season_type','season','week','receiving_tds','rushing_attempts']
allplayer_weekly = nfl.import_weekly_data(relevant_years)#, columns = relevant_data)

#%%
allplayer_weekly['fantasy_passing_pts'] = allplayer_weekly['passing_yards']*0.04+\
                                                 allplayer_weekly['passing_tds']*6+\
                                                     allplayer_weekly['passing_2pt_conversions']*2+\
                                                         allplayer_weekly['interceptions'] * -2 +\
                                                             allplayer_weekly['sack_fumbles_lost'] * -2
                                                             
allplayer_weekly['fantasy_halfppr_recieving_pts'] = allplayer_weekly['receiving_yards']*0.1+\
                                                 allplayer_weekly['receiving_tds']*6+\
                                                     allplayer_weekly['receiving_2pt_conversions']*2+\
                                                         allplayer_weekly['receptions'] * .5 +\
                                                             allplayer_weekly['receiving_fumbles_lost'] * -2
                                                             
allplayer_weekly['fantasy_rushing_pts'] = allplayer_weekly['rushing_yards']*0.1+\
                                                 allplayer_weekly['rushing_tds']*6+\
                                                     allplayer_weekly['rushing_2pt_conversions']*2+\
                                                         allplayer_weekly['rushing_fumbles_lost'] * -2
                                                                                                                                                                
                                 
allplayer_weekly['Calculated_Fantasy_Points'] = allplayer_weekly['fantasy_rushing_pts'] +\
                                                    allplayer_weekly['fantasy_halfppr_recieving_pts']+\
                                                        allplayer_weekly['fantasy_passing_pts']
                                                             
#%%

allplayer_weekly_pos = allplayer_weekly[allplayer_weekly['position'] == 'RB'].copy(deep = True)


pos_weekly_standings = pd.DataFrame()

pos_weekly_standings['player_id'] = allplayer_weekly_pos['player_id'].unique()
pos_weekly_standings['player_display_name'] = ''
for z in range(len(pos_weekly_standings['player_id'])):
    curr_label = pos_weekly_standings['player_id'][z]
    # print(curr_label)
    pos_weekly_standings['player_display_name'][z] = allplayer_weekly_pos[allplayer_weekly_pos['player_id'] == curr_label]['player_display_name'].unique()[0]
    # temp_out = allplayer_weekly_pos[allplayer_weekly_pos['player_id'] == curr_label]
    # pos_weekly_standings['player_display_name'] =  allplayer_weekly_pos[allplayer_weekly_pos['player_id'] in pos_weekly_standings['player_id']]['player_display_name']

#%%
for x,curr_year in enumerate(relevant_years):
    # print(x,curr_year)
# if True:
    
    
    all_player_weekly_singleseason = allplayer_weekly_pos[(allplayer_weekly_pos['season'] == curr_year) & (allplayer_weekly_pos['season_type'] == 'REG')].copy(deep = True)
    
    unique_players = all_player_weekly_singleseason['player_id'].unique()
    unique_weeks = all_player_weekly_singleseason['week'].unique()
    max_weeks = np.max(unique_weeks)
    for z in range(max_weeks):
        pos_weekly_standings[f'{curr_year}_{z+1}_FPTS'] = np.nan
        pos_weekly_standings[f'{curr_year}_{z+1}_FPTS_per_game'] = np.nan

        curr_dateframe = all_player_weekly_singleseason[all_player_weekly_singleseason['week'] <= z+1]
        
        
        curr_dataframe_out = curr_dateframe[['player_id','Calculated_Fantasy_Points']].groupby('player_id').sum()
        
        for p in range(len(curr_dataframe_out)):
            # curr_value = 
            pos_weekly_standings[f'{curr_year}_{z+1}_FPTS'][pos_weekly_standings['player_id'] ==curr_dataframe_out.index[p]] = curr_dataframe_out['Calculated_Fantasy_Points'][p]
            pos_weekly_standings[f'{curr_year}_{z+1}_FPTS_per_game'][pos_weekly_standings['player_id'] ==curr_dataframe_out.index[p]] = curr_dataframe_out['Calculated_Fantasy_Points'][p]/(z+1)

        
#%%

column_list = pos_weekly_standings.columns.tolist()

fpts_list = [x for x in column_list if 'FPTS' in x if 'per_game' not in x]
fpts_rank_list = [x for x in column_list if '_FPTS_per_game' in x]

column_rank_list = [x.replace('FPTS','Rank') for x in fpts_list]

iteration_list = fpts_rank_list
pos_weekly_standings[column_rank_list] = np.nan
for z in range(len(fpts_list)):
    curr_week_standings_no_out = pos_weekly_standings[['player_id',iteration_list[z]]].dropna().reset_index().drop(columns = ['index'])
    
    curr_week_standings_no_out['curr_week_rank'] = fff.sorting_dataframe(curr_week_standings_no_out,iteration_list[z])
    
    for p in range(len(curr_week_standings_no_out)):
        
        pos_weekly_standings[column_rank_list[z]][pos_weekly_standings['player_id'] == curr_week_standings_no_out['player_id'][p]] = curr_week_standings_no_out['curr_week_rank'][p]
        
        
        # pos_weekly_standings[column_rank_list[z]] = 

#%%
all_week_list = []
for k in range(1,16):
    
    
    temp_week_rank_list = [x for x in iteration_list if f'_{k}_' in x]
    
    end_week_rank_list = [x.replace(f'_{k}_','_17_') for x in iteration_list if f'_{k}_' in x]
    curr_week_list = []
    for i in range(len(temp_week_rank_list)):
        temp_out = pos_weekly_standings[pos_weekly_standings[temp_week_rank_list[i]].notna()][[temp_week_rank_list[i],end_week_rank_list[i]]]
        curr_week_list.append(temp_out.to_numpy())
    
    temp_out_2 = np.concatenate(curr_week_list)
    all_week_list.append(temp_out_2)
        
#%%
linregress_out = []
for z in range(len(all_week_list)):
    
    curr_fig = plt.figure()
    curr_ax = curr_fig.gca()
    x_vals = all_week_list[z][:,0]
    y_vals = all_week_list[z][:,1]
    curr_ax.scatter(x_vals,y_vals)
    curr_ax.set_xlabel(f'Rank_FPT upto week {z+1}')
    curr_ax.set_ylabel('Rank_FPT week 17')

    
    linregress_out.append(stats.linregress(x_vals,y_vals))
    print(linregress_out[z][3],linregress_out[z][2])


#%%

temporay_test = [[3,4],[6,7],[8,3]]        
        
        
        
#%%
curr_rb_seasons[f'{curr_year}_Rank'] = sorting_dataframe(curr_rb_seasons,'fantasy_points')


#%%
curr_rb_seasons = rb_season_data[rb_season_data['season']  == curr_year]
curr_rb_seasons[f'{curr_year}_Rank'] = sorting_dataframe(curr_rb_seasons,'fantasy_points')




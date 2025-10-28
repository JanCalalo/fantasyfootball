# -*- coding: utf-8 -*-
"""
Created on Thu May  8 19:03:59 2025

@author: Jan Calalo
"""


#%%

import nfl_data_py as nfl
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import scipy.optimize as opti
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.patches as patch


import data_visualization as dv

wheel = dv.ColorWheel()


#%% load all players

playernfl = nfl.import_players()

#%% load relevant years
relevant_years = np.arange(2010,2025).tolist()
relevant_data = ['player_id','position','receptions','targets','rushing_yards','receiving_yards',
                 'passing_yards','season_type','season','week','receiving_tds','rushing_attempts']
# player_catches_targets = nfl.import_weekly_data(relevant_years)#, columns = relevant_data)

allplayer_seasonal = nfl.import_seasonal_data(relevant_years,s_type = 'REG')

all_players_drafted = nfl.import_draft_picks(relevant_years)

#%% generate positional list from seasonal finishes

Selected_Position = 'TE'

#%% sorting player positions in outcomes
player_names = []
pos_out = []

draft_year = []
for x in range(len(allplayer_seasonal)):
    player_names.append(playernfl[playernfl['gsis_id'] == allplayer_seasonal['player_id'][x]]['display_name'].values[0])
    pos_out.append(playernfl[playernfl['gsis_id'] == allplayer_seasonal['player_id'][x]]['position'].values[0])
    
    
    curr_player_gsis_id = allplayer_seasonal['player_id'][x]
    if all_players_drafted['gsis_id'].isin([curr_player_gsis_id]).any():
        draft_year.append(all_players_drafted.loc[all_players_drafted['gsis_id'] == curr_player_gsis_id,'season'].values[0])    
    else:
        draft_year.append(np.nan)        
allplayer_seasonal['Player_Names'] = player_names
allplayer_seasonal['Positions'] = pos_out
allplayer_seasonal['Draft_Year'] = draft_year
#%% Generating list for just selected position

rb_season_data = allplayer_seasonal[allplayer_seasonal['Positions'] == Selected_Position][['player_id','games','season','Positions','Draft_Year','Player_Names','fantasy_points_ppr','fantasy_points']]
rb_season_data['Season_Finish'] = np.nan
rb_season_data['Season_Finish_HPPR'] = np.nan

rb_season_data['fantasy_points_hppr'] = (rb_season_data['fantasy_points'] + rb_season_data['fantasy_points_ppr'])/2

rb_season_data['FPG'] = rb_season_data['fantasy_points']/rb_season_data['games']
rb_season_data['FPG_HPPR'] = rb_season_data['fantasy_points_hppr']/rb_season_data['games']
rb_season_data['FPG_PPR'] = rb_season_data['fantasy_points_ppr']/rb_season_data['games']

#%%sorting rb seasons and getting their finishes
x = 0
curr_year = relevant_years[x]

for curr_year in relevant_years:
    # curr_rb_seasons = rb_season_data.query('season == curr_year')
    curr_rb_seasons = rb_season_data[rb_season_data['season']  == curr_year]
    
    sorted_curr_rb_season = curr_rb_seasons.sort_values('FPG',ascending = False).reset_index()
    # seasonal_rankings 
    
    for y in range(len(sorted_curr_rb_season)):
        curr_index = sorted_curr_rb_season['index'][y]
        rb_season_data.loc[curr_index,'Season_Finish'] = y+1

    # curr_rb_seasons = rb_season_data.query('season == curr_year')
    curr_rb_seasons = rb_season_data[rb_season_data['season']  == curr_year]
    
    sorted_curr_rb_season = curr_rb_seasons.sort_values('FPG_HPPR',ascending = False).reset_index()
    # seasonal_rankings 
    
    for y in range(len(sorted_curr_rb_season)):
        curr_index = sorted_curr_rb_season['index'][y]
        rb_season_data.loc[curr_index,'Season_Finish_HPPR'] = y+1

#%%

first_season_stats = rb_season_data.groupby('player_id').min('season')[['season']]
first_season_stats['average_finish'] = np.nan
first_season_stats['average_finish_years_2_4'] = np.nan
first_season_stats['average_FPG_years_2_4'] = np.nan
first_season_stats['Total_top_10s_years_2_4'] =np.nan

first_season_stats['average_FPG'] = np.nan
first_season_stats['average_FPG_HPPR'] = np.nan
first_season_stats['average_FPG_PPR'] = np.nan

first_season_stats['Total_top_10s'] =np.nan
# first_season_stats['fantasy_points_ppr'] = np.nan
# first_season_stats['fantasy_points'] =np.nan
first_season_stats['Player_Names'] = ''

first_season_stats['rookie_Finish'] =np.nan
first_season_stats['rookie_FPG'] =np.nan
first_season_stats['rookie_fantasy_points'] =np.nan
first_season_stats['rookie_fantasy_points_ppr'] =np.nan

drop_list = []
for i in range(len(first_season_stats)):
    
    curr_player_id = first_season_stats.iloc[i].name
    curr_player_rookie = first_season_stats.iloc[i]['season']
    single_players_seasons_data = rb_season_data.loc[rb_season_data['player_id'] == curr_player_id]
    
    
    if curr_player_rookie != single_players_seasons_data['Draft_Year'].values[0]:
        drop_list.append(curr_player_id)

    
    if len(single_players_seasons_data['season']) <= 1:
        # first_season_stats.drop(index = curr_player_id, inplace=True)
        
        drop_list.append(curr_player_id)
        # first_season_stats.iloc[i]['average_finish'] = np.nan

    else:
        
        single_players_seasons_data_exluding_rookie = single_players_seasons_data.loc[single_players_seasons_data['season'] != curr_player_rookie]
    
        first_season_stats.loc[curr_player_id,'Total_top_10s'] = len(single_players_seasons_data_exluding_rookie.loc[single_players_seasons_data_exluding_rookie['Season_Finish']<6])

        first_season_stats.loc[curr_player_id,'average_finish'] = np.nanmean(single_players_seasons_data_exluding_rookie['Season_Finish'])
        first_season_stats.loc[curr_player_id,'average_FPG'] = np.nanmean(single_players_seasons_data_exluding_rookie['FPG'])
        first_season_stats.loc[curr_player_id,'average_FPG_HPPR'] = np.nanmean(single_players_seasons_data_exluding_rookie['FPG_HPPR'])
        first_season_stats.loc[curr_player_id,'average_FPG_PPR'] = np.nanmean(single_players_seasons_data_exluding_rookie['FPG_PPR'])

        first_season_stats.loc[curr_player_id,'Player_Names'] = single_players_seasons_data_exluding_rookie['Player_Names'].values[0]
        

        first_season_stats.loc[curr_player_id,'rookie_Finish_HPPR'] = single_players_seasons_data.loc[single_players_seasons_data['season'] == curr_player_rookie,'Season_Finish_HPPR'].values[0]
        first_season_stats.loc[curr_player_id,'average_finish_HPPR'] = np.nanmean(single_players_seasons_data_exluding_rookie['Season_Finish_HPPR'])

        
        first_season_stats.loc[curr_player_id,'rookie_Finish'] = single_players_seasons_data.loc[single_players_seasons_data['season'] == curr_player_rookie,'Season_Finish'].values[0]
        first_season_stats.loc[curr_player_id,'rookie_fantasy_points'] = single_players_seasons_data.loc[single_players_seasons_data['season'] == curr_player_rookie,'fantasy_points'].values[0]
        first_season_stats.loc[curr_player_id,'rookie_fantasy_points_ppr'] = single_players_seasons_data.loc[single_players_seasons_data['season'] == curr_player_rookie,'fantasy_points_ppr'].values[0]
        first_season_stats.loc[curr_player_id,'rookie_FPG'] = single_players_seasons_data.loc[single_players_seasons_data['season'] == curr_player_rookie,'FPG'].values[0]
        first_season_stats.loc[curr_player_id,'rookie_FPG_HPPR'] = single_players_seasons_data.loc[single_players_seasons_data['season'] == curr_player_rookie,'FPG_HPPR'].values[0]
        first_season_stats.loc[curr_player_id,'rookie_FPG_PPR'] = single_players_seasons_data.loc[single_players_seasons_data['season'] == curr_player_rookie,'FPG_PPR'].values[0]

    max_season_av= 2
    if len(single_players_seasons_data['season']) >= max_season_av+1:
        
        if len(single_players_seasons_data_exluding_rookie.loc[single_players_seasons_data_exluding_rookie['season'] <= curr_player_rookie+max_season_av]) >= max_season_av: 
            
            single_players_seasons_data_exluding_rookie_up_to_four = single_players_seasons_data_exluding_rookie.loc[single_players_seasons_data_exluding_rookie['season'] <= curr_player_rookie+max_season_av]
            
            
            first_season_stats.loc[curr_player_id,'average_finish_years_2_4'] = np.nanmean(single_players_seasons_data_exluding_rookie_up_to_four['Season_Finish'])
            first_season_stats.loc[curr_player_id,'average_finish_HPPR_years_2_4'] = np.nanmean(single_players_seasons_data_exluding_rookie_up_to_four['Season_Finish_HPPR'])
    
            
            
            first_season_stats.loc[curr_player_id,'average_FPG_years_2_4'] = np.nanmean(single_players_seasons_data_exluding_rookie_up_to_four['FPG'])
            first_season_stats.loc[curr_player_id,'Total_top_10s_years_2_4'] = len(single_players_seasons_data_exluding_rookie_up_to_four.loc[single_players_seasons_data_exluding_rookie_up_to_four['Season_Finish']<6])
    
            first_season_stats.loc[curr_player_id,'average_FPG_HPPR_years_2_4'] = np.nanmean(single_players_seasons_data_exluding_rookie_up_to_four['FPG_HPPR'])
            first_season_stats.loc[curr_player_id,'average_FPG_PPR_years_2_4'] = np.nanmean(single_players_seasons_data_exluding_rookie_up_to_four['FPG_PPR'])
    

drop_list_uniques = list(set(drop_list))

for j in range(len(drop_list_uniques)):
    
        first_season_stats.drop(index = drop_list_uniques[j], inplace=True)
    
    
#%%

plt.figure()

plt.scatter(first_season_stats['rookie_Finish'],first_season_stats['average_finish'])    

stats_out = stats.pearsonr(first_season_stats['rookie_Finish'],first_season_stats['average_finish'])
plt.plot([0,120],[0,120])
    
print(stats_out)

#%%
plt.figure()

plt.scatter(first_season_stats['rookie_Finish'],first_season_stats['Total_top_10s'])    
stats_out = stats.pearsonr(first_season_stats['rookie_FPG'],first_season_stats['Total_top_10s'])
print(stats_out)

#%%

plt.figure()

plt.scatter(first_season_stats['rookie_FPG_HPPR'],first_season_stats['average_FPG_HPPR'])    
stats_out = stats.pearsonr(first_season_stats['rookie_FPG_HPPR'],first_season_stats['average_FPG_HPPR'])
print(stats_out)
# plt.plot([0,120],[0,120])
    
#%%
plt.figure()

plt.scatter(first_season_stats['rookie_FPG'],first_season_stats['average_FPG'])   
plt.plot([0,10],[0,10]  )


stats_out = stats.pearsonr(first_season_stats['rookie_FPG'],first_season_stats['average_FPG'])
print(stats_out)

# plt.plot([0,120],[0,120])

#%%



first_season_stats_year_2_to_4 = first_season_stats.dropna(inplace = False)


#%%

data_1 ='rookie_FPG_HPPR'
data_2 = 'average_FPG_HPPR_years_2_4'
plt.figure()

plt.scatter(first_season_stats_year_2_to_4[data_1],first_season_stats_year_2_to_4[data_2])    

stats_out = stats.pearsonr(first_season_stats_year_2_to_4[data_1],first_season_stats_year_2_to_4[data_2])
print(stats_out)

# plt.plot([0,120],[0,10])
tout = first_season_stats_year_2_to_4.loc[first_season_stats_year_2_to_4[data_2] >= 8][['Player_Names',data_1,data_2]]

print(tout)

plt.title(f'{data_1} v {data_2}') 

#%%

plt.figure()

plt.scatter(first_season_stats_year_2_to_4['rookie_FPG'],first_season_stats_year_2_to_4['average_FPG_years_2_4'])    

stats_out = stats.pearsonr(first_season_stats_year_2_to_4['rookie_FPG'],first_season_stats_year_2_to_4['average_FPG_years_2_4'])
plt.plot([0,10],[0,10])
    
print(stats_out)


plt.figure()

plt.scatter(first_season_stats_year_2_to_4['rookie_FPG_HPPR'],first_season_stats_year_2_to_4['average_FPG_HPPR_years_2_4'])    

stats_out = stats.pearsonr(first_season_stats_year_2_to_4['rookie_FPG_HPPR'],first_season_stats_year_2_to_4['average_FPG_HPPR_years_2_4'])
plt.plot([0,10],[0,10])
plt.title()
print(stats_out)


plt.figure()

plt.scatter(first_season_stats_year_2_to_4['rookie_FPG_PPR'],first_season_stats_year_2_to_4['average_FPG_PPR_years_2_4'])    

stats_out = stats.pearsonr(first_season_stats_year_2_to_4['rookie_FPG_PPR'],first_season_stats_year_2_to_4['average_FPG_PPR_years_2_4'])
plt.plot([0,10],[0,10])
    
print(stats_out)

#%%
fig = plt.figure()
ax = fig.add_axes([.1,.1,.8,.8])
ax.scatter(first_season_stats['rookie_FPG_HPPR'],first_season_stats['average_finish_HPPR'],color = wheel.blue)   

tout = first_season_stats.loc[first_season_stats['average_finish_HPPR'] <= 15][['Player_Names','average_finish_HPPR','rookie_FPG_HPPR']]

print(tout)



# ax.plot([0,10],[0,10])
# ax.axhline(10)


ax.set_xlim(-.1,12)
ax.set_ylim(0,120)
ax.axhline(12,color = wheel.grey, zorder = -10)
ax.set_xlabel('Rookie Year Fantasy Points Per Game (.5PPR)')

ax.set_ylabel('Average Ranking Year 2+')

ax.set_xticks(np.linspace(0,12.5,6))

dead_zone = patch.Rectangle([-.1,0],5.1,120,facecolor = wheel.red,alpha = .5,zorder = -100,edgecolor = wheel.none)

ax.add_patch(dead_zone)

ax.text(2.5,6,'Dead on Arrival',ha = 'center',va = 'center')

ax.spines[['top','right']].set_visible(False)
ax.set_title('Tight End Fantasy Outcomes (.5PPR)')
stats_out = stats.pearsonr(first_season_stats['rookie_FPG_HPPR'],first_season_stats['average_finish'])
print(stats_out)

# plt.plot([0,120],[0,120])
#%%
plt.figure()
plt.hist(first_season_stats['rookie_Finish_HPPR'],bins = np.arange(0,30)-.5)

first_season_stats.loc[first_season_stats['rookie_Finish_HPPR'] < 20]['Player_Names']
        
            
#%%

plt.figure()
plt.hist(first_season_stats['rookie_FPG_HPPR'],bins = np.arange(0,30)-.5)

first_season_stats.loc[first_season_stats['rookie_FPG_HPPR'] > 8][['Player_Names','average_FPG_HPPR']]   
    
    
    
    
    
    
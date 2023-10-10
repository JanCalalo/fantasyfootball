# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 20:46:48 2023

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


draft_picks = nfl.import_draft_picks()

#%%

ne_draft_picks = draft_picks.query("team == 'NWE' & position == 'WR' & season > 1990")


#%%

print(draft_picks.query("team == 'NWE' & position == 'WR' & season >= 1990 & rec_yards > 1000")[['pfr_player_name','season','round','rec_yards']])

#%%
print()

#%%
output_list= []
for x in draft_picks['team'].unique():
    curr_output = draft_picks.query(f"team == '{x}' & season >= 1990 & (allpro>0 or probowls > 0)")[['pfr_player_name','season','round','rec_yards']]
    
    curr_output_sum =  len(curr_output)
    
    output_list.append([x,curr_output_sum])
#%%

team_1000yards_rec = pd.DataFrame(output_list,columns = ['team','allpro_probowl'])

repeat_list = [['OAK','LVR','RAI'],
['PHO','ARI'],
['STL','RAM','LAR'],
['SDG','LAC']]


for curr_repeat_list in repeat_list:
    curr_name = curr_repeat_list[-1] + '_net'
    temp_sum = 0
    for z in curr_repeat_list:
        temp_sum += team_1000yards_rec[team_1000yards_rec['team'] == z]['allpro_probowl'].values[0]
        team_1000yards_rec.drop(team_1000yards_rec[team_1000yards_rec['team'] == z].index,inplace = True)
    new_df = pd.DataFrame.from_dict({'team': [curr_name], 'allpro_probowl':[temp_sum]}, orient='columns')
    team_1000yards_rec = pd.concat([team_1000yards_rec,new_df],ignore_index = True)
#%%  & position == 'LB'
x = 'SFO'
curr_output = draft_picks.query(f"team == '{x}' & season >= 1990 & (allpro>0 or probowls > 0)")[['pfr_player_name','season','round','probowls','allpro']]

print(curr_output)


#%%
l = [[1, 2, 3], [1, None, 4], [2, 1, 3], [1, 2, 2]]
df = pd.DataFrame(l, columns=["a", "b", "c"])
#%%



#%%

reset_names_draft_picks = fff.reset_team_names(draft_picks)
print(reset_names_draft_picks['team'].unique().shape)
#%%

since_season = 2000
above_3rd_round = np.where((reset_names_draft_picks.query(f'season >= {since_season}& (allpro>0 or probowls > 0)')['round'] > 3), 'Round 1-3', 'Round >=4')
# allpro > 0
selection_out = reset_names_draft_picks.query(f'season >= {since_season}& (allpro>0 or probowls > 0)').groupby(['team',above_3rd_round],group_keys = False,as_index = True).count().reset_index(drop=False, inplace=False)[['team','level_1','allpro','probowls']]



selection_out_sum = selection_out.groupby('team',as_index = False).sum()
selection_out_sum['level_1'] = 'All Rounds'


sorted_selection_out_sum = selection_out_sum.sort_values(by = 'allpro')
selection_out = pd.concat([selection_out,selection_out_sum]).sort_values(by = ['team','level_1']).reset_index(drop = True)  
# selection_out_sum = 
# selection_out = reset_names_draft_picks.query(f'season >= {since_season}& (allpro>0 or probowls > 0)').groupby(['team',above_3rd_round],group_keys = True,as_index = True).count()[['allpro','probowls']]



#%%
repeat_list = [['OAK','LVR','RAI'],
['PHO','ARI'],
['STL','RAM','LAR'],
['SDG','LAC']]


for curr_repeat_list in repeat_list:
    curr_name = curr_repeat_list[-1] + '_net'
    temp_sum = 0
    for z in curr_repeat_list:
        temp_sum += selection_out[selection_out['team'] == z]['allpro']
        selection_out.drop(selection_out[selection_out['team'] == z].index,inplace = True)
    new_df = pd.DataFrame.from_dict({'team': [curr_name], 'allpro':[temp_sum]}, orient='columns')
    selection_out = pd.concat([selection_out,new_df],ignore_index = True)



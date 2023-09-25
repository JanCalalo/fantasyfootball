# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 21:36:06 2023

@author: Jan Calalo
"""

import nfl_data_py as nfl
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import scipy.optimize as opti
#%%
relevant_years = np.arange(2017,2023).tolist()
relevant_data = ['player_id','position','receptions','targets','rushing_yards','receiving_yards',
                 'passing_yards','season_type','season','week','receiving_tds','rushing_attempts']
# player_catches_targets = nfl.import_weekly_data(relevant_years)#, columns = relevant_data)

test_out = nfl.import_seasonal_data(relevant_years)

playernfl = nfl.import_players()

#%%
player_names = []
pos_out = []
for x in range(len(test_out)):
    player_names.append(playernfl[playernfl['gsis_id'] == test_out['player_id'][x]]['display_name'].values[0])
    pos_out.append(playernfl[playernfl['gsis_id'] == test_out['player_id'][x]]['position'].values[0])
    
#%%

test_out['Player_Names'] = player_names
test_out['Positions'] = pos_out

#%%

rb_out = test_out[test_out['Positions'] == 'RB']

#%%

rb_out['RYPC'] = rb_out['rushing_yards']/rb_out['carries']


#%%

rb_out_min5 = rb_out[rb_out['carries'] > 50]
#%%

players_of_interest = ['Derrick Henry',
                       'Alexander Mattison',
                       # "Le'Veon Bell",
                       "Dalvin Cook",
                       # 'Josh Jacobs'
                        'David Montgomery','Tony Pollard','Nick Chubb',
                       ]

color_list = ['blue','red','purple','green','#ff34f3','orange']

plt.figure()

plt.scatter(rb_out_min5['carries'],rb_out_min5['RYPC'],facecolor = 'none',edgecolor = 'black',alpha = .5)
Player_Of_Interest_Carries = []
for p in range(len(players_of_interest)):
    curr_player_of_interest = rb_out_min5[rb_out_min5['Player_Names'] == players_of_interest[p]]
    Player_Of_Interest_Carries.append(curr_player_of_interest)

                                      
    plt.scatter(curr_player_of_interest['carries'],curr_player_of_interest['RYPC'],color = color_list[p],label= players_of_interest[p])
    

plt.legend(ncol = 2)

plt.xlabel('Season Carries 2017-2023 (Min 50)')
plt.ylabel('Season RYPC')





# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 22:59:34 2023

@author: Jan Calalo
"""


import nfl_data_py as nfl
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import scipy.optimize as opti
import pandas as pd
import matplotlib.pyplot as plt

#%% load all players

playernfl = nfl.import_players()

#%% load relevant years
relevant_years = np.arange(2023,2024).tolist()
relevant_data = ['player_id','position','receptions','targets','rushing_yards','receiving_yards',
                 'passing_yards','season_type','season','week','receiving_tds','rushing_attempts']
allplayer_weekly = nfl.import_weekly_data(relevant_years)#, columns = relevant_data)

allplayer_seasonal = nfl.import_seasonal_data(relevant_years,s_type = 'REG')

#%%

alloff_weekly = allplayer_weekly.query("position in ['QB','RB','WR','TE']")
alloff_weekly[['passing_epa','receiving_epa','rushing_epa']] = alloff_weekly[['passing_epa','receiving_epa','rushing_epa']].fillna(0)
#%%
alloff_weekly['OFF_epa'] = alloff_weekly['passing_epa']  + alloff_weekly['receiving_epa']  +alloff_weekly['rushing_epa']   

# alloff_weekly['nonqb_OFF_epa'] = alloff_weekly['passing_epa']  + alloff_weekly['receiving_epa']  +alloff_weekly['rushing_epa']   

#%%

allplayer_sorted_offensive_epa = alloff_weekly.sort_values('OFF_epa',ascending = False).reset_index()
nonqb_sorted_offensive_epa = alloff_weekly[alloff_weekly['position'] != 'QB'].sort_values('OFF_epa',ascending = False).reset_index()

#%%

for x in range(50):
    selected_row = nonqb_sorted_offensive_epa.iloc[x]
    
    
    print(selected_row[['player_display_name','season','week','OFF_epa']])
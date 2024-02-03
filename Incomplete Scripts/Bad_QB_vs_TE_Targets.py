# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:21:42 2023

@author: Jan Calalo
"""

import nfl_data_py as nfl
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import scipy.optimize as opti
#%% Load Weekly  TE targets



get_pbp_cols = nfl.see_pbp_cols()

pbp_cols = ['week','play_id','play_type','passer_player_name','receiver_player_name','passer_id','receiver_id','pass_length','sack','pass_attempt']
years = [2022]

current_pbp_data = nfl.import_pbp_data(years,pbp_cols)



#%% sync to weekly targets


unique_games = current_pbp_data.nflverse_game_id.unique()


#%%
selected_game = unique_games[0]
select_pbp_game = current_pbp_data[current_pbp_data['nflverse_game_id'] == selected_game]

selected_pbp_game_pass = select_pbp_game[select_pbp_game['play_type'] == 'pass']

#%% 
ngs_data = nfl.import_ngs_data('passing',[2022])

season_data = nfl.import_seasonal_data([2022], s_type='REG')

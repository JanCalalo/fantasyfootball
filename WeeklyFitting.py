#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 13:44:47 2023

@author: jacccalalo
"""
import nfl_data_py as nfl
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import scipy.optimize as opti
#%%
relevant_years = np.arange(2017,2023).tolist()
relevant_data = ['player_id','position','receptions','targets','rushing_yards','receiving_yards','passing_yards','season_type','season','week','receiving_tds']
player_catches_targets = nfl.import_weekly_data(relevant_years, columns = relevant_data)

#%%
playernfl = nfl.import_players()
#%%
Player_name = "Ja'Marr Chase"
# Player_name = 'Lamar Jackson'
# Player_name = 'Justin Fields'

select_player = playernfl[playernfl['display_name'] == Player_name]
#%%
player_catches_targets = player_catches_targets[player_catches_targets['position'] == 'WR']
player_catches_targets_wr = player_catches_targets[player_catches_targets['season_type'] == 'REG']
# player_catches_targets_wr = player_catches_targets[player_catches_targets['targets'] > 0]

metric_of_interest = ['receptions']

# metric_of_interest = ['rushing_yards','passing_yards']
#%%
cumulative = True
if cumulative:
    Title = 'CDF'
else:
    Title = 'PDF'
curr_fig = plt.figure()
curr_ax = plt.gca()
rushing_list = player_catches_targets_wr[metric_of_interest[0]].to_numpy()
# passing_list = player_catches_targets_wr[metric_of_interest[1]].to_numpy()
passing_list = 0 #player_catches_targets_wr[metric_of_interest[1]].to_numpy()

reception_list = np.zeros_like(rushing_list)
for x in range(len(rushing_list)):
    reception_list[x] = rushing_list[x] +  0
    
curr_max = np.max(reception_list)
x_fit= np.arange(0,curr_max+2)-.5


binned_data = curr_ax.hist(reception_list,x_fit,density = True,cumulative= cumulative,color = 'grey')




data_out = stats.beta.fit(reception_list,fscale = curr_max+2)


a = data_out[0]
b = data_out[1]
x = np.arange(0,curr_max+1)


beta_out = stats.beta(a,b,scale = curr_max+2)
new_ax = curr_ax.twinx()

x_plot = np.arange(0,curr_max+1)
if cumulative:
    beta_data_out = beta_out.cdf(x)
else:
    beta_data_out = beta_out.pdf(x)
    
new_ax.plot(x_plot,beta_data_out,color = 'black')

curr_ax.set_ylim(0,1)
# 
# new_ax.set_ylim(0,1)

plt.show()

player_catches_targets 
selected_catches_targets_wins = player_catches_targets_wr[player_catches_targets_wr['player_id'] == select_player['gsis_id'].to_list()[0]]
specific_player_reception_list = selected_catches_targets_wins[metric_of_interest].to_numpy()

rushing_list_specific = selected_catches_targets_wins[metric_of_interest[0]].to_numpy()
# passing_list_specific = selected_catches_targets_wins[metric_of_interest[1]].to_numpy()
passing_list_specific = 0# selected_catches_targets_wins[metric_of_interest[1]].to_numpy()
 
reception_list_specific = np.zeros_like(rushing_list_specific)
for x in range(len(reception_list_specific)):
    reception_list_specific[x] = rushing_list_specific[x] + 0
    
binned_data_2 = curr_ax.hist(reception_list_specific,x_fit,density = True,cumulative= cumulative,color = 'blue',alpha = .2)

data_out_2 = stats.beta.fit(reception_list_specific,fscale = curr_max+2)

a = data_out_2[0]
b = data_out_2[1]
x = np.arange(0,curr_max+1)


beta_out_2 = stats.beta(a,b,scale = curr_max+2)
# new_ax = curr_ax.twinx()
if cumulative:
    beta_data_out_2 = beta_out_2.cdf(x)
else:
    beta_data_out_2 = beta_out_2.pdf(x)

new_ax.plot(x_plot,beta_data_out_2,color = 'blue')

# curr_ax.set_ylim(0,1)

# new_ax.set_ylim(0,1)
plt.show()

curr_ax.set_xlim([0,curr_max])
curr_ax.set_xticks(np.linspace(0,curr_max,5))
curr_ax.set_ylim(0,np.nanmax([binned_data[0],binned_data_2[0]]))
# curr_ax.set_yticks(np.linspace(0,1,6))
joint_pdf = np.array([beta_data_out,beta_data_out_2])
joint_pdf = joint_pdf[np.isfinite(joint_pdf)]
new_ax.set_ylim(0,np.nanmax(joint_pdf))
# new_ax.set_yticks(np.linspace(0,1,6))

curr_ax.set_ylabel(Title)
curr_ax.set_xlabel(metric_of_interest)
curr_ax.set_title(Player_name)
plt.show()

#%%
stats.ks_2samp(beta_out.cdf(x),beta_out_2.cdf(x))

max(specific_player_reception_list)
#%%
plt.figure()
curr_ax = plt.gca()
generate_counts = np.zeros(curr_max+1) *np.nan

for i in range(curr_max+1):
    generate_counts[i] = (reception_list ==i).sum()



curr_ax.plot(np.arange(0,curr_max+1),np.cumsum(generate_counts)/np.sum(generate_counts))


selected_catches_targets_wins = player_catches_targets_wr[player_catches_targets_wr['player_id'] == select_player['gsis_id'].to_list()[0]]
specific_player_reception_list = selected_catches_targets_wins['receptions'].to_numpy()
generate_counts = np.zeros(curr_max+1) *np.nan

for i in range(curr_max+1):
    generate_counts[i] = (specific_player_reception_list ==i).sum()



curr_ax.plot(np.arange(0,curr_max+1),np.cumsum(generate_counts)/np.sum(generate_counts))



curr_ax.set_xlim(0,16)
curr_ax.set_xticks(np.arange(0,17))
curr_ax.set_ylim(0,1)
curr_ax.set_yticks(np.linspace(0,1,6))


curr_ax.
# stats.cdf(x

#%%

Y_Data = player_catches_targets_wr['receiving_yards'].to_numpy()

X_Data = player_catches_targets_wr['receptions'].to_numpy()


Y_Data_spec = selected_catches_targets_wins['receiving_yards'].to_numpy()

X_Data_spec = selected_catches_targets_wins['receptions'].to_numpy()

#%%
plt.figure()
plt.scatter(X_Data,Y_Data,color = 'grey')

plt.scatter(X_Data_spec,Y_Data_spec,color = 'blue')
plt.show()
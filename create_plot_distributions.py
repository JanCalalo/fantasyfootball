import nfl_data_py as nfl
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import scipy.optimize as opti
import pandas as pd
import nfl_plot_py as nflplt
import data_visualization as dv
import json
import requests as rq
import time
# %%

player_list= rq.get("https://api.sleeper.app/v1/players/nfl").json()
player_list_dict = pd.DataFrame.from_dict(player_list,orient='index')
active_players_sleeper_dataframe = player_list_dict[player_list_dict['status'] != 'Inactive']

#%%
list_of_leagues = ["https://sleeper.app/draft/nfl/1209304724965163008",
"https://sleeper.app/draft/nfl/1201718378352361472",
"https://sleeper.app/draft/nfl/1199759549511249920",
"https://sleeper.app/draft/nfl/1197693853444866048",
"https://sleeper.app/draft/nfl/1193411848941219840",
"https://sleeper.app/draft/nfl/1187169108436099072",
"https://sleeper.app/draft/nfl/1186432468747427840",
"https://sleeper.app/draft/nfl/1181415067647049729",
"https://sleeper.app/draft/nfl/1185678639152422912",
"https://sleeper.app/draft/nfl/1180333578234331137",
"https://sleeper.app/draft/nfl/1180191025385660417",
"https://sleeper.app/draft/nfl/1180125892624809985",
"https://sleeper.com/draft/nfl/1180273953490202625",
"https://sleeper.app/draft/nfl/1182497792344498177",
"https://sleeper.com/draft/nfl/1182392767111606273"]

# generate_league__ids

draft_ids = []
for x in range(len(list_of_leagues)):

    curr_id = list_of_leagues[x].split('/')[-1]
    draft_ids.append(curr_id)




#%%
i = 12
all_draft_dataframes = pd.DataFrame()
for i in range(len(list_of_leagues)):
    response = rq.get(f"https://api.sleeper.app/v1/draft/{draft_ids[i]}/picks")
    # GET https://api.sleeper.app/v1/draft/<draft_id>/picks
    out = response.json()# %%
    time.sleep(.01)

    single_draft_dataframe = pd.json_normalize(out)
    all_draft_dataframes = pd.concat([all_draft_dataframes,single_draft_dataframe])


#%%

Interesting_Players_list = ['Ashton Jeanty','Travis Hunter','Omarion Hampton','Cameron Ward','Tetairoa McMillan']#,'TreVeyon Henderson']
Interesting_Players_list = ['Ashton Jeanty','Travis Hunter','Omarion Hampton']

list_player_ids = []
for i in range(len(Interesting_Players_list)):
    player_name = Interesting_Players_list[i]
    player_id = active_players_sleeper_dataframe[active_players_sleeper_dataframe['full_name'] == player_name]['player_id'][0]
    list_player_ids.append(player_id)
    print(i,player_name,player_id)
#%%
fig = plt.figure()
curr_ax = fig.add_axes([.1,.1,.8,.8])


colors = [wheel.autumn,wheel.teal,wheel.lavender,wheel.red,wheel.dark_blue]
curr_ax.spines[['right', 'top']].set_visible(False)


curr_ax.set_xlabel(f'Pick No.')
curr_ax.set_ylabel('Frequency')
curr_ax.set_xticks(np.arange(1,11))

curr_ax.set_xlim(-.1,10.1)

Density = True
if Density:
    curr_ax.set_ylim(0, 1)
    curr_ax.set_yticks(np.arange(0,1.01,.25))

    norm = 15
else:
    curr_ax.set_ylim(0, 15)
    curr_ax.set_yticks(np.arange(0,16,3))
    norm = 1
bins = np.arange(-.5,11.5,1)
for i in range(len(Interesting_Players_list)):
    curr_array = all_draft_dataframes[all_draft_dataframes['player_id'] == list_player_ids[i]]['pick_no'].values


    curr_ax.hist(curr_array,bins = bins,alpha = .5,bottom = 0,density = Density,
                 align = 'mid',histtype = 'step',lw = 5,facecolor = '.5',edgecolor =colors[i])#,edgealpha = 1)
    


dv.Custom_Legend(curr_ax,Interesting_Players_list,colors[0:len(Interesting_Players_list)])




curr_ax.annotate("Jeanty's been drafted 1.01\n100% of the time",xy = (1.8,13/norm), xytext = (2.8,13/norm),
                 arrowprops = dict(facecolor = colors[0],edgecolor = wheel.none),
                 ha = "left",va = "center",color = colors[0])

curr_ax.annotate("Travis is Pretty Evenly\nSpread Between 2-4",xy = (5,5/norm), xytext = (6,7/norm),
                 arrowprops = dict(facecolor = colors[1],edgecolor = wheel.none),
                 ha = "left",va = "center",color = colors[1])


curr_ax.set_title(f"Current Distribution of Draft Picks\n({len(list_of_leagues)} Leagues)")
# %%

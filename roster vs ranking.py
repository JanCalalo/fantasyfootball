"""
Jan Calalo

"""


#%%
import requests
import pandas as pd
import numpy as np

username = 'ShutTheDoor'
#%%
player_list= requests.get("https://api.sleeper.app/v1/players/nfl").json()

#%%

league_ID = 808099427142213632
league_ID = 1180273953490202624
#%%
r = requests.get(f"https://api.sleeper.app/v1/league/{league_ID}/matchups/{week}")


u = requests.get("https://api.sleeper.app/v1/league/"+str(league_ID)+"/users")
users = pd.DataFrame.from_records(u.json())
#%%
returned = requests.get("https://api.sleeper.app/v1/league/"+str(league_ID)+"/rosters")

rosters = pd.DataFrame.from_records(returned.json())


# %%

my_owner_id = str(606709838843572224)


my_roster = rosters[rosters['owner_id'] == my_owner_id]

my_players = my_roster['players'].values[0]
#%%

player_list_df = pd.DataFrame.from_dict(player_list,orient = "index")
#%%
my_players_dataframe = pd.DataFrame(my_players)
my_players_dataframe.columns = ['player_id']
my_players_dataframe['Name'] = ''


my_players_dataframe['Positions'] = ''

 
for i in range(len(my_players_dataframe)):
    
    curr_player = my_players_dataframe['player_id'][i]

    curr_player_data  = player_list_df.loc[curr_player]

    print(curr_player_data['full_name'],curr_player_data['fantasy_positions'])

    my_players_dataframe.loc[i]['Name'] = curr_player_data['full_name']
    temp_string = ''
    for j,x in enumerate(curr_player_data['fantasy_positions']):

        if j == 0:
            temp_string = x
        else:
            temp_string = temp_string +'_' + x
    my_players_dataframe.loc[i]['Positions'] = temp_string

#%%

my_players_dataframe[my_players_dataframe['Positions'].str.contains('DB')]

    
# %%

rankings = pd.read_csv('2025_idp_rankings.csv')
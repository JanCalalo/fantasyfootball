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

player_list_df = pd.DataFrame.from_dict(player_list,orient = "rows")
#%%
my_players_dataframe = pd.DataFrame(my_players)

my_players_dataframe['Names'] = ''


my_players_dataframe['Positions'] = ''


for i in range(len(my_players_dataframe)):




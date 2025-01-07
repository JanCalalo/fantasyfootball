"""
Get Player Names from Sleeper
For Upload to Google Sheets
"""


import requests
import os
import pandas as pd
if True:
    player_list= requests.get("https://api.sleeper.app/v1/players/nfl").json()


player_list_dict = pd.DataFrame.from_dict(player_list,orient='index')
active_players_sleeper_dataframe = player_list_dict[player_list_dict['status'] != 'Inactive']


curr_folder = os.getcwd()
active_players_sleeper_dataframe.to_csv(os.path.join(curr_folder,'Local_Files','2024_Players.csv'))

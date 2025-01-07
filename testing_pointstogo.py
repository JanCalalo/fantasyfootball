# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 19:57:30 2023

@author: Jan Calalo
"""


import requests
import pandas as pd
import numpy as np

username = 'Calalo'
#%%
player_list= requests.get("https://api.sleeper.app/v1/players/nfl").json()

#%%

league_ID = 808099427142213632
league_ID = 967289105010753536
week = 4
r = requests.get(f"https://api.sleeper.app/v1/league/{league_ID}/matchups/{week}")


u = requests.get("https://api.sleeper.app/v1/league/"+str(league_ID)+"/users")
users = pd.DataFrame.from_records(u.json())

rosters = pd.DataFrame.from_records(requests.get("https://api.sleeper.app/v1/league/"+str(league_ID)+"/rosters"))
#%%
weekmatchups = pd.DataFrame.from_records(r.json()) 

['1373',
 '7528',
 '8132',
 '5846',
 '5872',
 '9756',
 '5844',
 '8137',
 '5012',
 '8160']

#%%
pd.DataFrame.from_records(requests.get("https://api.sleeper.app/v1/league/"+str(league_ID)).json())


#%%

temp_out = requests.get("https://api.sleeper.app/v1/league/"+str(league_ID)).json()
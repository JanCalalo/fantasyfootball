# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 13:52:40 2023

@author: Jan
"""

import numpy as np

def isthatboynice(Player_Name):
    """
    

    Parameters
    ----------
    Player_Name : String
        DESCRIPTION.

    Returns
    -------
    ISTHATBOYNICE : String {"Yes, No, Mid"}
        Answer to how nice boy is. 
        

    """
    
    thresh = np.random.uniform(0,1)

    player_val = np.random.uniform(0,1)


    if player_val-thresh <  -.1:
        ISTHATBOYNICE = "NO" 
    elif player_val-thresh >  .1:
        ISTHATBOYNICE = "YES" 
    else:
        ISTHATBOYNICE = "MID"
        
    print(f"IS {player_name} NICE? {ISTHATBOYNICE}")

    return ISTHATBOYNICE
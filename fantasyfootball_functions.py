# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 19:22:10 2023

@author: Jan Calalo
"""




import pandas as pd
import numpy as np

def sorting_dataframe(input_dataframe,sorting_column):
    
    curr_dataframe = input_dataframe.copy(deep = True)
    curr_dataframe['Rank'] = np.nan
    sorted_dataframe = curr_dataframe.sort_values(sorting_column,ascending = False).reset_index()
    for y in range(len(sorted_dataframe)):
        curr_index = sorted_dataframe['index'][y]
        curr_dataframe['Rank'][curr_index] = y+1
    
    
    
    return curr_dataframe['Rank']

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


#%% sync to weekly targets

#%% 
ngs_data = nfl.import_ngs_data('passing',[2022])

season_data = nfl.import_seasonal_data([2022], s_type='REG')

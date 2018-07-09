#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 16:44:49 2018

@author: boris
"""

import connect4class

#%%
# 3 vs Random
connect4class.run_experiment(experiment_name='3vs0',
               polt_every_nth=100,
               num_games = 10000,
               players_to_use_MinMax = [1],
               max_depth=[3],
               board_size = [19,19])
#%%
# 3vs1
connect4class.run_experiment(experiment_name='3vs1',
               polt_every_nth=2,
               num_games = 10000,
               players_to_use_MinMax = [1,-1],
               max_depth=[3,1],
               board_size = [19,19])
#%%
# 3vs2
connect4class.run_experiment(experiment_name='3vs2',
               polt_every_nth=1,
               num_games = 10000,
               players_to_use_MinMax = [1,-1],
               max_depth=[3,2],
               board_size = [19,19])
#%%
# 3vs3
connect4class.run_experiment(experiment_name='3vs3',
               polt_every_nth=2,
               num_games = 10,
               players_to_use_MinMax = [1,-1],
               max_depth=[3,3],
               board_size = [19,19])
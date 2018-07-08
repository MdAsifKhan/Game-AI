#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 14:00:25 2018
A simple stop watch

@author: boris
"""
import time
# https://docs.python.org/3/library/time.html#time.time

class PausableTimer:
    """A simple pausable timer"""
    def __init__(self):
        self.t = 0.0
        
    def pause(self):
        end = time.time()
        self.total_time = self.t + (end - self.start)
        return self.t
        
    def resume(self):
        self.start = time.time()
    
    def reset(self):
        self.t = 0.0

#Some test code: 
'''       
tt = PausableTimer()
tt.resume()
time.sleep(1)
print(tt.pause())
time.sleep(2)
tt.resume()
time.sleep(4)
print(tt.pause())
'''
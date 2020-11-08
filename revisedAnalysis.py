import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
from time import sleep
import random
import os
from statsmodels.graphics.gofplots import qqplot
import scipy
from scipy.stats import ttest_ind, ttest_rel, f_oneway
from tabulate import tabulate


Uber2019 = pd.read_csv('UberOCT7.csv')
Uber2019 = Uber2019.drop(columns=['segment_id', 'start_junction_id', 'end_junction_id', 'osm_start_node_id', 'osm_end_node_id'])

counts = {}

for i in Uber2019['road_name']:
    if i in counts:
        counts[i] += 1
    else:
        counts[i] = 1
    
    
count_list = {k: v for k, v in sorted(counts.items(), key=lambda item: item[1])}
list(count_list)[-10:]


class UniqueRoadway:
    def __init__(self, name, df):
        
        if len(name) == 1:
            colname = list(name.keys())[0]
            value = list(name.values())[0]
            
            self.df = df[df[colname] == value]
            self.name = value
        
    def review(self, num1, num = 0):
        display(self.df[num:num1])
        return
        
    def cols(self):
        return self.df.columns
    
    def anova_oneway(self, colname):
        
        li = [kamiti[kamiti.hour_of_day == i][colname] for i in range(24)]
            
        stat, p = scipy.stats.f_oneway(*li)
        print('Statistics=%.3f, p=%.3f' % (stat, p))
        
        # interpret
        alpha = 0.05
        if p > alpha:
            print('Same distributions (fail to reject H0)')
        else:
            print('Different distributions (reject H0)')
            
    def hour_of_day(self, num):
        
        return self.df[self.df.hour_of_day == num]
    
    def morning_commute(self):
        
        temp = pd.DataFrame()
        
        for i in range(6,10):
            
            t = self.df[self.df.hour_of_day == i]
            
            temp = temp.append(t, sort=False)
        
        return temp
    
    def evening_commute(self):
        
        temp = pd.DataFrame()
        
        for i in range(17,22):
            
            t = self.df[self.df.hour_of_day == i]
            
            temp = temp.append(t, sort=False)
        
        return temp

    def t_test(self, var1, var2, label_dict = {}):
        
        twosample_results = scipy.stats.ttest_ind(var1, var2)
        
        if twosample_results[1] <= 0.05:
            print("The difference between means is statistically significant.")
        
        if label_dict:
            if len(label_dict) == 1:
                key = list(label_dict.keys())[0]
                value = list(label_dict.values())[0]
                
                tbl = pd.DataFrame(columns=['Comparison', 'Test Statistic', 'P-Value'])
                
                temp = {'Comparison': f"{key} vs. {value}", 'Test Statistic': twosample_results[0], 'P-Value': twosample_results[1]}
                
                tbl = tbl.append(pd.DataFrame([temp]), sort=False)
                
                display(tbl)
                
                return tbl
            
        else:
            
            tbl = pd.DataFrame(columns=['Test Statistic', 'P-Value'])

            temp = {'Test Statistic': twosample_results[0], 'P-Value': twosample_results[1]}

            tbl = tbl.append(pd.DataFrame([temp]), sort=False)
            
            display(tbl)

            return tbl
            
            
magadi = UniqueRoadway({'road_name':'Magadi Road'}, Uber2019)

magadi_morn = magadi.morning_commute()
magadi_eve = magadi.evening_commute()

magadi_ttest = magadi.t_test(magadi_morn['speed_kph_p85'], magadi_eve['speed_kph_p85'], {'Magadi Road Morning Commute':'Evening Commute'})

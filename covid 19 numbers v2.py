#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 10)

import matplotlib.pyplot as plt

from numpy import log as ln


# In[2]:


get_ipython().system('rm /home/cjd/COVID19/*.csv')
get_ipython().system('wget https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')
get_ipython().system('wget https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')


# In[3]:


cases = pd.read_csv('/home/cjd/COVID19/time_series_19-covid-Confirmed.csv')
cases = cases.drop(columns=['Lat', 'Long'])
cases = pd.concat([cases.groupby('Country/Region').sum()])
cases = cases.sort_values(by=[cases.columns[-1]], ascending=False)
cases


# In[4]:


deaths = pd.read_csv('/home/cjd/COVID19/time_series_19-covid-Deaths.csv')
deaths = deaths.drop(columns=['Lat', 'Long'])
deaths = pd.concat([deaths.groupby('Country/Region').sum()])
deaths = deaths.sort_values(by=[deaths.columns[-1]], ascending=False)
deaths


# In[5]:


top_ten = cases.index[0:10].tolist()
calc = pd.DataFrame()
calc['Cases'] = cases.loc[top_ten,cases.columns[-1]]
calc['Deaths'] = deaths.loc[top_ten,deaths.columns[-1]]
calc['Case Fatality Rate'] =  (calc['Deaths'] / calc['Cases']) * 100.0
calc = calc.sort_values(by=['Case Fatality Rate'], ascending=False).round(1)
calc


# In[6]:


cases_doubling_time = ln(2)/ln(1 + cases.loc[top_ten,:].pct_change(axis='columns'))
cases_doubling_time = cases_doubling_time.loc[ :, cases.columns[-10:] ]
cases_doubling_time.sort_values(by=[cases_doubling_time.columns[-1]]).round(1)


# In[7]:


deaths_doubling_time = ln(2)/ln(1 + deaths.loc[top_ten,:].pct_change(axis='columns'))
deaths_doubling_time = deaths_doubling_time.loc[ :, deaths.columns[-10:] ]
deaths_doubling_time.sort_values(by=[deaths_doubling_time.columns[-1]]).round(1)


# In[8]:


get_ipython().run_line_magic('matplotlib', '')

country_list = [
'US', 
'Korea, South',
'Italy',
'Spain',
'France',
'United Kingdom',   
'Germany',
    
# 'United Kingdom',
# 'China',
# 'Iran',
]

styles = ['b-','g-.','k--','r:','m.-','co-','ys-']

for i,name in enumerate(country_list):

#         ax = cases.loc[ name, : ].plot()
    ax = cases.loc[ name, cases.columns[-30:] ].plot(style=styles[i])
#     ax = case_doubling_time.loc[ name, case_doubling_time.columns[-30:] ].plot()


ax.set_xlabel('Date', fontsize=20)
ax.set_ylabel('Number of Cases', fontsize=20)

ax.legend(country_list, loc='upper left', fontsize=20)

ax.grid(True, alpha=0.25)

plt.show()


# In[9]:


# pop_list = [
#     {'Country/Region': 'US', 'population': 327.2e6}, 
#     {'Country/Region': 'China', 'population': 1.386e9},
#     {'Country/Region': 'Italy', 'population': 360.48e6},
#     {'Country/Region': 'Iran', 'population': 81.16e6},
#     {'Country/Region': 'Spain', 'population': 46.66e6},
#     {'Country/Region': 'United Kingdom', 'population': 66.44e6},
#     {'Country/Region': 'France', 'population': 66.99e6},
#     {'Country/Region': 'Switzerland', 'population': 8.57e6},
#     {'Country/Region': 'Korea, South', 'population': 51.47e6},
#     {'Country/Region': 'Germany', 'population': 82.79e6},
# ]

# pop = pd.DataFrame(pop_list)

# temp = pd.merge(pop, calc, on='Country/Region')

# temp['Cases as % of Pop.'] = temp['Cases'] / (temp['population']/100)

# temp.sort_values(by=['Cases as % of Pop.'], ascending=False).round(3)


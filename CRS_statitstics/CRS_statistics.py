import requests 
from bs4 import BeautifulSoup 
import parsing_tools
import plotting_tools

import pandas as pd 

URL = "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/submit-profile/rounds-invitations/results-previous.html"
r = requests.get(URL) 
soup = BeautifulSoup(r.content, 'html5lib') 

body = soup.find('div', attrs = {'class': 'mwsgeneric-base-html parbase section'})
rows = body.find_all('p')
rows_list = list(rows)

## define when website changed its form (from 77th round)
## all entries for dict are found using <p> - in old version of the site there are
## 226 <p>, so need to exclude them using [:-226] - this will exclude last 76 rounds 
old_rounds = 226
## creates a dict with form {datetime.datetime(year, month, day, hours, min, sec): 
## [score, num of invitations]}
fsw_scores_dict = parsing_tools.parsing_string(rows_list[:-old_rounds])
old_fsw_scores_dict = parsing_tools.old_crs_parser()
fsw_scores_dict.update(old_fsw_scores_dict)

## forming to pandas dataframe 
dates = {'Date':[x for x in fsw_scores_dict.keys()]}
scores = []
ranks = []
for value_list in fsw_scores_dict.values():
    scores.append(value_list[0])
    ranks.append(value_list[1])
fsw_df = pd.DataFrame({'Date of invitation':[x for x in fsw_scores_dict.keys()], 
                       'Scores': scores, 'Number of invitations (Top #)': ranks})
## formating Date to datetime and separation years to a new column
fsw_df['Date of invitation'] = pd.to_datetime(fsw_df['Date of invitation'], format='%Y %m %d')
fsw_df.insert(loc =0, column = 'Year', value = fsw_df['Date of invitation'].apply(lambda x: x.year))

## plotting
plotting_tools.plot_crs_stats(fsw_df)

## analysis
print(fsw_df.groupby('Year')['Scores'].describe())
print('\nLatest round: (', fsw_df.iloc[0,1], ')\n', fsw_df.iloc[0,2:])

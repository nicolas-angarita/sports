import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import json

import time
import random



def nfl_data_scrape(season_beg_year = None, season_end_year = None):
    
    if season_beg_year is None:
        season_beg_year = int(input("Enter the first year of the season you want to collect data from: "))
    if season_end_year is None:
        season_end_year = int(input('Enter the last year of the season you want to collect data from: ')) + 1
    
    
    # create the list of seasons to download 
    seasons = [str(season) for season in range (season_beg_year, season_end_year)]
    

    # create the list of team abbreviations
    team_abbrs =['crd','atl','rav','buf','car','chi','cin','cle', 'dal','den','det','gnb','htx',
                 'clt','jax','kan', 'sdg','ram','rai','mia','min', 'nwe','nor','nyg','nyj','phi',
                 'pit','sea','sfo','tam','oti','was']
    
    print(f'Number Of Seasons = {len(seasons)}')
    print(f'Number Of Teams = {len(team_abbrs)}')
    
    
    #create an empty df to append
    nfl_df = pd.DataFrame()

    #iterate through the seasons
    with tqdm(total=len(team_abbrs), desc="Processing NFL Seasons", unit="Season") as pbar:
        for season in seasons:
            #iterate through the teams
            for team in team_abbrs:
                #Step 1. Set the URL
                url = 'https://www.pro-football-reference.com/teams/' + team + '/' + season + '/gamelog/'

                try:
                    #Step 2. Get offensive stats (from game logs table)
                    off_df = pd.read_html(url, header=1, attrs={'id':'gamelog' + season})[0]

                    #Step 3. Get the defensive stats (from opponents Game logs table)
                    def_df = pd.read_html(url, header=1, attrs ={'id': 'gamelog_opp' + season})[0]

                    #Step 4. Concat the two dataframes (Offensive and defensive) (along columns, axis = 1)
                    team_df = pd.concat([off_df, def_df], axis =1)

                    #Insert the season to the df
                    team_df.insert(loc=0, column = 'season', value= season)

                    #Insert the team to the df
                    team_df.insert(loc=1, column = 'team', value = team.upper())

                    #Step 5. Concat the team gamelog to the aggregate df (along rows, axis = 0)
                    nfl_df = pd.concat([nfl_df,team_df], ignore_index=True)

                    #pause the program to abide by the website rules 
                    time.sleep(random.randint(7,8))        

                except ValueError as e:
                    print("No tables found on the page:", e)
                    
                pbar.update(1)

    
    return nfl_df




def clean_data(csv_data):
    
    '''
    This function takes in data in csv format and transformers it into a df and cleans it up with column 
    removals, renaming, and adding more context to column data
   
    csv_data: should be the full data set collected to pass the whole df through the fucntion to 
    make sure it's cleaned the with the correct format
   
    
    '''

    # read in data in form of csv data
    df = pd.read_csv(csv_data)
    
    #drop repeated columns information
    df.drop(df.columns[38:48], axis=1, inplace=True)
    
    #drop unnecessary column of 'boxscore'
    df.drop(columns= ['Unnamed: 3'], axis = 1, inplace=True)
    
    #lowercase all column names
    df.columns = df.columns.str.lower()
    
    #rename column names
    df.rename(columns={'unnamed: 4': 'result','unnamed: 6': 'host', 'tm':'pts','opp.1':'opp_pts',
                       'cmp':'pass_cmp', 'att':'pass_att','yds':'pass_yds','td':'pass_td',
                       'yds.1':'yds_lost_sks','y/a':'yds_pass_att', 'ny/a':'net_yds_pass_att',
                       'rate':'pass_rating', 'att.1':'rush_att', 'yds.2': 'rush_yds',
                       'y/a.1':'rush_yds_att','td.1':'rush_td','yds.3':'punt_yds'}, inplace = True)

    # List of original column names
    renamed_columns = ['pass_cmp', 'pass_att', 'pass_yds', 'pass_td', 'int', 'sk', 'yds_lost_sks',
                       'yds_pass_att','net_yds_pass_att', 'cmp%', 'pass_rating', 'rush_att', 'rush_yds',
                       'rush_yds_att', 'rush_td', 'fgm', 'fga', 'xpm', 'xpa', 'pnt', 'punt_yds',
                       '3dconv', '3datt', '4dconv', '4datt', 'top']

    # Add '_opp' to each name
    new_column_names = [col + '_opp' for col in renamed_columns]

    # Renaming columns in the DataFrame
    df.rename(columns=dict(zip(df.columns[37:], new_column_names)), inplace = True)
    
    #replace nan values with home and @ with away to show which are home games or away
    df['host'] = df['host'].apply(lambda x: 'away' if x == '@' else 'home')
    
    #replace nan values with yes or no values accoriding to ot results
    df['ot'] = df['ot'].apply(lambda x: 'yes' if x == 'OT' else ' no')
    
    return df






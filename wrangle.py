import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import json
from datetime import datetime 
import time
import random



def nfl_data_scrape(season_beg_year = None, season_end_year = None, filename = None):
    '''
    This function will scrape raw data from https://www.pro-football-reference.com. It will prompt you to put in the 
    season you want data to from the beginning year to ending year. (i.e. 2000 - 2010 for the 2000 to the 2010 season.
    Or if you just want 2023 data it would be 2023 for beginning year and 2023 for ending year) Then you will be
    prompted to input a filename to save as a csv file. There will be a progress bar to show how far you are along the 
    scraping process
    '''
    # input code lines for respective variables to run the function 
    if season_beg_year is None:
        season_beg_year = int(input("Enter the first year of the season you want to collect data from: "))
    if season_end_year is None:
        season_end_year = int(input('Enter the last year of the season you want to collect data from: ')) + 1
    if filename is None:
        filename = str(input('Enter a filename for this data to save as a csv file (no need to add extenison of file): ')).strip() + '.csv'
    
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

                    #Step 4. Concat the two dataframes (Offensive and defensive) along columns
                    team_df = pd.concat([off_df, def_df], axis =1)

                    #Insert the season to the df
                    team_df.insert(loc=0, column = 'season', value= season)

                    #Insert the team to the df
                    team_df.insert(loc=1, column = 'team', value = team.upper())

                    #Step 5. Concat the team gamelog to the aggregate df along rows
                    nfl_df = pd.concat([nfl_df,team_df], ignore_index=True)

                    #pause the program to abide by the website rules 
                    time.sleep(random.randint(7,8))        

                except ValueError as e:
                    print("No tables found on the page:", e)
                    
                pbar.update(1)

    # df is saved to a csv file
    nfl_df.to_csv(filename, index= False)

    # Print the filename
    print(f"Data will be saved as: {filename}")
    
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
    
    #drop repeated columns information **look into this in the future as I dont think this will work for multiple seasons
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


# Function to convert "minutes:seconds" to total seconds
def convert_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds


# Function to convert the date column to datetime and parser date information 
def parse_month_day_with_season(row):
    try:
        # Parse the date string
        date = datetime.strptime(row['date'], "%B %d")
        # Set the year from the 'season' column
        return date.replace(year=row['season'])
    except ValueError:
        return pd.NaT


def final_cleaned_df(df):

    '''
    This Function takes in a dataframe after its been initially cleaned by the clean_data function. Also, using the
    convert_to_seconds & parse_month_day_with_seasons functions to enable this function to run smoothly. This function
    will also be calling in the csv file that contains all prior data from the 2000 - 2023 seasons. This csv file will be
    updated as more seasons go by and we collect more data.

    This function will perform the last stage of cleaning the dataset in the way we want it for modeling, by mapping,
    removing columns, renaming columns, creating a game_id, making home teams / away teams columns, stats, etc.

    '''
    
    # team abbr to team names - mapping to create columns later in the function
    team_code_map = {
    'CRD': 'Arizona Cardinals',
    'ATL': 'Atlanta Falcons',
    'RAV': 'Baltimore Ravens',
    'BUF': 'Buffalo Bills',
    'CAR': 'Carolina Panthers',
    'CHI': 'Chicago Bears',
    'CIN': 'Cincinnati Bengals',
    'CLE': 'Cleveland Browns',
    'DAL': 'Dallas Cowboys',
    'DEN': 'Denver Broncos',
    'DET': 'Detroit Lions',
    'GNB': 'Green Bay Packers',
    'CLT': 'Indianapolis Colts',
    'JAX': 'Jacksonville Jaguars',
    'KAN': 'Kansas City Chiefs',
    'SDG': 'Los Angeles Chargers',
    'RAM': 'Los Angeles Rams',
    'RAI': 'Las Vegas Raiders',
    'MIA': 'Miami Dolphins',
    'MIN': 'Minnesota Vikings',
    'NWE': 'New England Patriots',
    'NOR': 'New Orleans Saints',
    'NYG': 'New York Giants',
    'NYJ': 'New York Jets',
    'PHI': 'Philadelphia Eagles',
    'PIT': 'Pittsburgh Steelers',
    'SEA': 'Seattle Seahawks',
    'SFO': 'San Francisco 49ers',
    'TAM': 'Tampa Bay Buccaneers',
    'OTI': 'Tennessee Titans',
    'WAS': 'Washington Commanders',
    'HTX': 'Houston Texans'
    }

    # Step 1: Replace team abbreviations in the 'team' column with full names
    df['team_full_name'] = df['team'].map(team_code_map)

    # Step 2: Create a unique identifier for each game
    # This ensures each game is represented only once, even if it's recorded from both teams' perspectives
    df['game_id'] = df.apply(lambda row: f"{row['season']}_{row['week']}_{'_'.join(sorted([row['team_full_name'], row['opp']]))}", axis=1)

    # Step 3: Drop duplicate entries based on the game_id
    # Keep only one entry for each game (e.g., keeping the first occurrence)
    df = df.drop_duplicates(subset='game_id', ignore_index= True)
    
    
    # Step 3: Make home and away columns 
    df['home_team'] = df.apply(lambda row: row['team_full_name'] if row['host'] == 'home' else row['opp'], axis = 1)
    df['away_team'] = df.apply(lambda row: row['opp'] if row['host'] == 'home' else row['team_full_name'], axis = 1)

    # Step 4 Since we are dealing with future data that data does not exist yet to be able to predict on / work with
    df.fillna(0, inplace=True)
    
    # Step 5: Values should be an int and make it into a str ('0:0') to be able to convert to seconds 
    df.loc[df['top'] == 0, 'top'] = '0:0'
    df.loc[df['top_opp'] == 0, 'top_opp'] = '0:0'
    
    # Step 6: Apply the function to the 'top' column
    df['total_top'] = df['top'].apply(convert_to_seconds)
    df['opp_total_top'] = df['top_opp'].apply(convert_to_seconds)

    # Step 7: Create the home_results column to show if home teams won or lost 
    df['home_results'] = ((df['result'] == 'W') & (df['host'] == 'home')) | ((df['result'] == 'L') & (df['host'] == 'away'))
    df['home_results'] = df['home_results'].astype(int)

    # Step 8: Apply the parser to the DataFrame to work with a datetime object to manipluate date
    df['parsed_date'] = df.apply(parse_month_day_with_season, axis=1)

    # Step 9: Making columns for season, day of week, and month
    df['season'] = df['parsed_date'].dt.year
    df['day_of_week'] = df['parsed_date'].dt.dayofweek
    df['month'] = df['parsed_date'].dt.month

    # Step 10: Encoded overtime column 
    df['ot'] = df['ot'].apply(lambda x: 1 if x == 'yes' else 0)

    # Step 11: Game id is redone so that the home team always comes first then the away team
    df['game_id'] = df.apply(lambda row: f"{row['season']}_{row['week']}_{'_'.join([row['home_team'], row['away_team']])}", axis=1)


    # Step 12 & 13: Create and assign statistics for home and away teams
    stats_columns = ['pts', 'pass_cmp', 'pass_att', 'pass_yds', 'pass_td', 'int', 'sk',
                     'yds_lost_sks', 'yds_pass_att','net_yds_pass_att', 'cmp%', 'pass_rating', 'rush_att',
                     'rush_yds','rush_yds_att', 'rush_td', 'fgm', 'fga', 'xpm', 'xpa', 'pnt','punt_yds', '3dconv',
                     '3datt', '4dconv', '4datt', 'total_top']
    opp_stats_columns = ['opp_pts','pass_cmp_opp', 'pass_att_opp', 'pass_yds_opp', 'pass_td_opp','int_opp', 'sk_opp',
                         'yds_lost_sks_opp', 'yds_pass_att_opp','net_yds_pass_att_opp', 'cmp%_opp', 'pass_rating_opp',
                         'rush_att_opp','rush_yds_opp', 'rush_yds_att_opp', 'rush_td_opp', 'fgm_opp', 'fga_opp',
                         'xpm_opp', 'xpa_opp', 'pnt_opp', 'punt_yds_opp', '3dconv_opp','3datt_opp', '4dconv_opp',
                         '4datt_opp', 'opp_total_top']

    # Step 14: Line is needed to make sure the stats go to the correct team
    df['home_is_team'] = df['home_team'] == df['team_full_name']

    # Step 15: Assigning stats to home and away team 
    for team_stat, opp_stat in zip(stats_columns, opp_stats_columns):
        df[f'home_{team_stat}'] = df.apply(lambda row: row[team_stat] if row['home_is_team'] else row[opp_stat], axis=1)
        df[f'away_{team_stat}'] = df.apply(lambda row: row[opp_stat] if row['home_is_team'] else row[team_stat], axis=1)

    # Step 17: Dropping columns
    df = df.drop(columns=stats_columns + opp_stats_columns + ['date','team_full_name','home_is_team','team','day',
                                                          'result','host','opp','top','top_opp'])

    # Step 18: Renaming columns 
    df.rename(columns = {'parsed_date': 'date', 'ot':'overtime','home_total_top': 'home_top',
                         'away_total_top': 'away_top'},inplace = True)

    # Step 19: Create a column for point difference
    df['pts_diff_home'] = df['home_pts'] - df['away_pts']
    
    # Step 20: Create a column for passing yards difference
    df['pass_yds_diff_home'] = df['home_pass_yds'] - df['away_pass_yds']
    
    # Step 21: Create a column for rushing yards difference
    df['rush_yds_diff_home'] = df['home_rush_yds'] - df['away_rush_yds']
    
    # Step 22: Create a column for time of possession difference
    df['top_diff_home'] = df['home_top'] - df['away_top']             # Steps 19 - 22 are the perspective of home team
                                                                      # I.E. if negative than away team had x AMT more
    # Step 23: Create a column for total yards by home team
    df['home_total_yds']= df['home_pass_yds'] + df['home_rush_yds']
    
    # Step 24: Create a column for total yards by away team
    df['away_total_yds']= df['away_pass_yds'] + df['away_rush_yds']

    # Step 25: Bring in older csv dataset from previous seasons 
    old_data = pd.read_csv('nfl_data_2000_2023_seasons.csv')
    
    # Step 26: Get the common columns in the order they appear in old_data df
    common_columns = [col for col in old_data.columns if col in df.columns]

    # Step 27: Get the additional columns in df that are not in old_data (look in future as this might not be needed)
    additional_columns = [col for col in df.columns if col not in old_data.columns]

    # Step 28: Reorder df columns
    df = df[common_columns + additional_columns]
    
    # Step 29: Edit the year on Jan games that should be + 1 year i.e. 2024 should be jan 3, 2025, then reset index
    jan_games = df['month'] == 1
    df.loc[jan_games, 'date'] = df.loc[jan_games, 'date'] + pd.DateOffset(years=1)
    df.reset_index(drop= 'index',inplace=True)
    
    # Step 30: Sort the data by the date
    df = df.sort_values(by='date', ascending=True, ignore_index=True)
    
    return df


    # Notes
    # Read in csv files with this format to get dt object 
        # pd.read_csv(filename, parse_dates=['date'], date_format='%Y-%m-%d')







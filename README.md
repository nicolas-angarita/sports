# <div align="center">The Love of the Game </div>

<br>

<img src="https://ravenswire.usatoday.com/wp-content/uploads/sites/55/2019/12/gettyimages-1193623120.jpg?w=1000&h=600&crop=1" alt="Lamar Jackson">

# Project Goals

 - Indentify what features or factors most influence NFL Games outcomes
 - Build a model to best predict the winner of a NFL game
 - Build a model to best predict vegas lines (over/under & moneyline) of a NFL game 


# Project Description

We are looking to build multiple supervised and unsupervised machine learning models using different algorithms to accurately predict outcomes of NFL games.
Then using our models to place bets and hopefully make some money! I've grew up playing, watching, and enjoying football; mix that with my interests in data and naturally you get my interest in finding out if there's any
factors that most contribute to winning an NFL game. Anyone that is apart of the NFL, or sports world really, has heard "Defense Wins Championships." So does the data actually back that up or did someone just happen to say that one 
season after watching their team dominate. We are going to find out if defenses really are a major factor or does the data tell us otherwise. Within the project we won't only be looking for features that help us predict what influences a team to win, 
but we're going to take it a step further. When and if we find any features that actually contribute to a team's success, could that help us make bets to win against the most common vegas lines? These lines will include the over/under, moneyline,
and eventually the spread of a game. We'll explain a little more about what these mean later on. 

Project Quote: 'Show me the data'

# Initial Questions

 1. What features influence the most for a team to win?
 2. Do those features help us predict the outcomes of other NFL games?
 3. Can we use those features to predict outcomes when  we want to place bets against the most common vegas lines?
 4. Are we able to find the over/under outcome with accuracy?
 5. Out of 1000 bets what would be our outcome on the moneyline bets be for the 2023 season?
 6. Will our 2024 predictions have at least a 55% accuracy?


# The Plan

 - Create README with project goals, project description, initial hypotheses, planning of project, data dictionary, and come up with recommedations/takeaways

### Acquire Data
 - Acquire data from stathead.com. From this database I will create a function to scrape the necessary data that I need to carry out this project.
 - Then I will create a function to scrape updated data to be able to run this for future seasons. These functions will go into a juptyer notebook. (acquire.py)

### Prepare Data
 - Clean and prepare the data creating a function that will give me data that is ready to be explored upon. Within this step we will also write a function to split our data into train, validate, and test. (prepare.py) 
 


## Data Dictionary


| Target Variable |     Definition     |
| --------------- | ------------------ |
|      home_results    | 0 refers to the away team winning and 1 refers to the home team winning |

| Feature  | Definition |
| ------------- | ------------- |
| game_id | a unique identifier for each game played with the season, week, home team, and away team |
| home_team | the home team for that game  |
| away_team | the away team for that game |
| date | date of the game played on |
| season | the year the season was played  |
| month | refers to the month the game played in (i.e. 10 = October, 12 = December) | 
| week | refers to the week of the NFL season |
| day_of_week | refers to the day the game was played on (i.e. 0 = Monday - 6 = Sunday) |
| overtime | 0 refers to no overtime and 1 refers to yes there was overtime in the game |
| home_pts | refers to the amount of points the home team scored  |
| away_pts | refers to the amount of points the away team scored |
| home_pass_cmp | home team passing completions |
| away_pass_cmp | away team passing completions |
| home_pass_att | home team passing attempts |
| away_pass_att | away team passing attempts |
| home_pass_yds | home team passing yards |
| away_pass_yds | away team passing yards |
| home_pass_td | home team passing touchdowns |
| away_pass_td | away team passing touchdown  |
| home_int | home team interceptions thrown |
| away_int | away team interceptions thrown |
| home_sk | home team allowed sacks |
| away_sk | away team allowed sacks |
| home_yds_lost_sks | home team lost yards from sacks |
| away_yds_lost_sks | away team lost yards from sacks |
| home_yds_pass_att | home team yards per pass attempt |
| away_yds_pass_att | away team yards per pass attempt  |
| home_net_yds_pass_att | home team net yards per pass | 
| away_net_yds_pass_att | away team net yards per pass |
| home_cmp% | home team passing completion percent|
| away_cmp% | away team passing completion percent |
| home_pass_rating | home team passer rating  |
| away_pass_rating | away team passer rating | 
| home_rush_att | home team rushing attempts |
| away_rush_att | away team rushing attempts |
| home_rush_yds | home team rushing yards |
| away_rush_yds | away team rushing yards  |
| home_rush_yds_att | home team rushing yards per attempt |
| away_rush_yds_att | away team rushing yards per attempt |
| home_rush_td | home team rushing touchdowns |
| away_rush_td | away teams rushing touchdowns  |
| home_fgm | home team field goals made |
| away_fgm | away team field goals made |
| home_fga | home team field goals attempts |
| away_fga | away team field goals attempts  |
| home_xpm | home team extra points made  |
| away_xpm | away team extra points made |
| home_xpa | home team extra points attempts |
| away_xpa | away team extra points attempts |
| home_pnt | home team number of punts  |
| away_pnt | away team number of punts |
| home_punt_yds | home team punt yards |
| away_punt_yds | away team punt yards |
| home_3dconv | home team 3rd down conversions |
| away_3dconv | away team 3rd down conversions | 
| home_3datt | home team 3rd down attempts |
| away_3datt | away team 3rd down attempts |
| home_4dconv  | home team 4th down conversions  |
| away_4dconv | away team 4th down conversions |
| home_4datt | home team 4th down attempts |
| away_4datt | away team 4th down attempts |
| home_top | home team time of possession  |
| away_top | away team time of possession |
| pts_diff_home | points differential in perspective of the home team (i.e. -5 means the away team scored 5 more points than the home team, 7 means the home team scored 7 more points than the away team) |
| pass_yds_diff_home | passing yards differential in perspective of the home team (i.e. negative passing yards means the away team had that number more of the home team, positive yards means the home team had that many more passing yards than the away team) |
| rush_yds_diff_home | rushing yards differential in the perspective of the home team(i.e. (i.e. negative rushing yards means the away team had that number more of the home team, positive yards means the home team had that many more rushing yards than the away team) |
| top_diff_home | time of possession differential in the perspective of the home team(i.e. negative time means the away team had that more of time of possession than the home team, if the time is positive that means the home team had that amount of time of possession more than the away team.) Also, time is recorded in seconds |
| home_total_yds | home team total passing and rushing yards |
| away_total_yds | away team total passing and rushing yards |


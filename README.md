# <div align="center">The Love of the Game </div>

<br>

*https://ravenswire.usatoday.com/wp-content/uploads/sites/55/2019/12/gettyimages-1193623120.jpg?w=1000&h=600&crop=1*

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
|      btc_price    | price of Bitcoin |

| Feature  | Definition |
| ------------- | ------------- |
| open | Opening price of the asset |
| high | The high price point of the asset  |
| low | The low price point of the asset |
| close | The closing price of the asset |
| adj close | The closing price after adjustments  |
| volume | The amount of an asset that changes hands | 
| dji_price | The price of the Dow Jones Industrial Average |
| gold | The price of gold per ounce|

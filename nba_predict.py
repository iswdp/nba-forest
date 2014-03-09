from nba import as_dict, arrange_dict, validate_nba, team_aggregates, arrange_aggregates
from scraper import scrape_nba, scrape_aggre
from pandas import DataFrame
import pandas as pd

team_ids = {'POR':1610612757, 'LAC':1610612746, 'HOU':1610612745, 'MIN':1610612750, 'OKC':1610612760, 'PHX':1610612756, 'MIA':1610612748, 'DAL':1610612742, 'SAS':1610612759, 'GSW':1610612744, 'DEN':1610612743, 'ATL':1610612737, 'LAL':1610612747, 'SAC':1610612758, 'DET':1610612765, 'WAS':1610612764, 'TOR':1610612761, 'PHI':1610612755, 'NOP':1610612740, 'IND':1610612754, 'BKN':1610612751, 'NYK':1610612752, 'CLE':1610612739, 'ORL':1610612753, 'MEM':1610612763, 'BOS':1610612738, 'CHA':1610612766, 'UTA':1610612762, 'MIL':1610612749, 'CHI':1610612741}
symbols = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
cols = ['Date', 'Team', 'Opponent', 'WL', 'vs', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

#scrape_nba()
#scrape_aggre()
print 'Converting downloaded data to dictionary-----------------'
cumsums = as_dict(symbols, cols)
aggs = team_aggregates()

for i in symbols:
    temp = []
    for j in range(len(cumsums[i])):
        temp.append(aggs[i]['W%'][0])
    temp = DataFrame(temp)
    temp.columns = ['W%']
    cumsums[i] = pd.concat([cumsums[i], temp], axis=1)

print 'Arranging data--------------------------------------------'
arrange_dict(cumsums, symbols)
validate_nba(trees=100, workers=1)
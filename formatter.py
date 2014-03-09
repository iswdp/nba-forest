import json
import pandas as pd
from pandas import DataFrame

#Put team data into a dictionary---------------------------------------------------------------------------------------------------------------------
loaded_data = json.load(open('dictdata.txt'))
symbols = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
cols = ['Date', 'Team', 'Opponent', 'WL', 'vs', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
cumsums = {}

for k in symbols:
    x = loaded_data[k]
    team = []

    for i in range(len(x)-1):
        formatted = [str(x[i][2])]
        temp = str(x[i][3]).split()
        formatted.append(temp[0])
        formatted.append(temp[2])
        formatted.append(str(x[i][4]))

        if temp[1] == 'vs.':
            temp[1] = 0
        else:
            temp[1] = 1
            
        formatted.append(temp[1])
        for j in range(5,24):
            formatted.append(float(x[i][j]))
        team.append(formatted)

    team.reverse()
    cumsums[k] = DataFrame(team, columns = cols)

#----------------------------------------------------------------------------------------------------------------------------------------------------

cols = cumsums['ATL'].columns.tolist()
cols2 = (cumsums['ATL'].ix[:,5:].columns + '1').tolist()
cols.extend(cols2)
ATL = DataFrame(columns = cols)

for team in symbols:
    for Date in cumsums[team]['Date']:
        Opponent = cumsums[team].ix[cumsums[team]['Date'] == Date, 'Opponent'].all()

        for Opponent_Date in cumsums[Opponent]['Date']:
            if Opponent_Date == Date:
                op_index = cumsums[Opponent].ix[cumsums[Opponent]['Date'].copy() == Date].ix[:,5:].index[0] - 1
                te_index = cumsums[team].ix[cumsums[team]['Date'].copy() == Date].ix[:,0:].index[0] - 1

                try:
                    op_temp = DataFrame(cumsums[Opponent].ix[op_index, 5:]).T
                    te_temp = DataFrame(cumsums[team].ix[te_index, 0:]).T
                    te_temp['Date'] = Date
                    te_temp['Opponent'] = cumsums[team].ix[te_index + 1,'Opponent']
                    te_temp['WL'] = cumsums[team].ix[te_index + 1,'WL']
                    op_temp = op_temp.reset_index()
                    te_temp = te_temp.reset_index()
                    op_temp = op_temp.ix[:,1:]
                    te_temp = te_temp.ix[:,1:]
                    op_temp.columns = op_temp.columns + '1'
                    atl = pd.concat([te_temp, op_temp], axis = 1)
                    ATL = pd.concat([ATL, atl], axis = 0)
                    break        
        
                except:
                    break

    print team

ATL.to_csv('final.csv', sep=',', index=False)
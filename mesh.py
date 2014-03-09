import pandas as pd
from pandas import DataFrame

symbols = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

cumsums = {}

for i in symbols:
    cumsums[i] = pd.read_csv('cumsums/' + i + '.csv').ix[15:,:]

cols = cumsums['ATL'].columns.tolist()
cols2 = (cumsums['ATL'].ix[:,4:].columns + '1').tolist()
cols.extend(cols2)
ATL = DataFrame(columns = cols)

for team in symbols:
    for Date in cumsums[team]['Date']:
        Opponent = cumsums[team].ix[cumsums[team]['Date'] == Date, 'Opponent'].all()

        for Opponent_Date in cumsums[Opponent]['Date']:
            if Opponent_Date == Date:
                op_index = cumsums[Opponent].ix[cumsums[Opponent]['Date'].copy() == Date].ix[:,4:].index[0] - 1
                te_index = cumsums[team].ix[cumsums[team]['Date'].copy() == Date].ix[:,0:].index[0] - 1

                try:
                    op_temp = DataFrame(cumsums[Opponent].ix[op_index, 4:]).T
                    te_temp = DataFrame(cumsums[team].ix[te_index, 0:]).T
                    te_temp['Date'] = Date
                    te_temp['Opponent'] = cumsums[team].ix[te_index + 1,'Opponent']
                    te_temp['W/L'] = cumsums[team].ix[te_index + 1,'W/L']
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

ATL.to_csv('train1.csv', sep=',', index=False)
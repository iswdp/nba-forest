#Contains functions for nba predictions
import json
from pandas import DataFrame
from pandas import Series
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def team_aggregates():
    team_ids = {'POR':1610612757, 'LAC':1610612746, 'HOU':1610612745, 'MIN':1610612750, 'OKC':1610612760, 'PHX':1610612756, 'MIA':1610612748, 'DAL':1610612742, 'SAS':1610612759, 'GSW':1610612744, 'DEN':1610612743, 'ATL':1610612737, 'LAL':1610612747, 'SAC':1610612758, 'DET':1610612765, 'WAS':1610612764, 'TOR':1610612761, 'PHI':1610612755, 'NOP':1610612740, 'IND':1610612754, 'BKN':1610612751, 'NYK':1610612752, 'CLE':1610612739, 'ORL':1610612753, 'MEM':1610612763, 'BOS':1610612738, 'CHA':1610612766, 'UTA':1610612762, 'MIL':1610612749, 'CHI':1610612741}
    loaded_data = json.load(open('aggre_data.txt'))
    key = team_ids.keys()[team_ids.values().index(1610612757)]

    aggre_dict = {}
    headers = ['W%', 'FGM', 'FGA', 'FG%', '3FGM', '3FGA', '3FG%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS', 'O/U']

    for i in loaded_data['rowSet']:
        key = team_ids.keys()[team_ids.values().index(i[0])]
        aggre_dict[key] = Series(i)
        aggre_dict[key] = aggre_dict[key].drop(0)
        aggre_dict[key] = aggre_dict[key].drop(1)
        aggre_dict[key] = aggre_dict[key].drop(2)
        aggre_dict[key] = aggre_dict[key].drop(3)
        aggre_dict[key] = aggre_dict[key].drop(4)
        aggre_dict[key] = aggre_dict[key].drop(6)
        aggre_dict[key] = aggre_dict[key].drop(28)
        aggre_dict[key] = aggre_dict[key].drop(29)
        aggre_dict[key] = aggre_dict[key].reset_index()
        aggre_dict[key] = aggre_dict[key].drop('index', axis=1)
        aggre_dict[key] = DataFrame(aggre_dict[key]).T
        aggre_dict[key].columns = headers
        print key

    return aggre_dict

def as_dict(symbols, cols):
    loaded_data = json.load(open('dictdata.txt'))
    cumsums = {}

    for k in symbols:
        print k
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

        #Calculate cumulative averages-------------------------
        for i in range(6,24):
            for j in range(len(cumsums[k].ix[:,1])):
                try:
                    #cumsums[k].ix[j,i] = cumsums[k].ix[0:j,i].mean()
                    cumsums[k].ix[j,i] = cumsums[k].ix[0:len(cumsums[k].ix[:,1]),i].mean()

                except:
                    break

        mins = []
        for i in range(len(cumsums[k].ix[:,1])):
            mins.append(cumsums[k].ix[0:i,5].sum())
        for i in range(len(cumsums[k].ix[:,1])):
            cumsums[k].ix[i,5] = mins[i]

    return cumsums

def arrange_dict(cumsums, symbols):
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

def arrange_aggregates(cumsums, symbols, aggs):
    for i in symbols:
        cumsums[i] = cumsums[i].ix[:,0:5]

    cols = cumsums['ATL'].columns.tolist()
    cols2 = aggs['ATL'].columns.tolist()
    cols3 = (aggs['ATL'].columns + '1').tolist()
    cols.extend(cols2)
    cols.extend(cols3)
    ATL = DataFrame(columns = cols)

    for team in symbols:
        for Date in cumsums[team]['Date']:
            Opponent = cumsums[team].ix[cumsums[team]['Date'] == Date, 'Opponent'].all()
            cumsums_temp = cumsums[team].ix[cumsums[team]['Date'] == Date]
            cumsums_temp = cumsums_temp.reset_index()
            team_temp = aggs[team]
            oppenent_temp = DataFrame(aggs[Opponent])
            oppenent_temp.columns = cols3
            atl = pd.concat([cumsums_temp, team_temp, oppenent_temp], axis = 1)
            atl = atl.drop('index', axis=1)
            atl.columns = cols
            ATL = pd.concat([ATL, atl], axis = 0)

        print team

    ATL.to_csv('final.csv', sep=',', index=False)

def validate_nba(trees=5, workers=1):
    print 'Validating predictions.'
    data = pd.read_csv('final.csv')
    m = RandomForestClassifier(n_estimators = trees, n_jobs=workers)

    predictions = []
    tally = []

    for i in range(0,len(data.ix[:,0])):
        train = data.drop(i, axis = 0)
        test = DataFrame(data.ix[i,:]).T

        m.fit(train.ix[:,4:], train.ix[:,'WL'])
        current_pred = m.predict(test.ix[:,4:])[0]
        predictions.append(current_pred)
        if str(current_pred) == str(test.ix[:,3].values[0]):
            tally.append(1)
        else:
            tally.append(0)
        current_score = round((float(sum(tally))/len(tally)) * 100, ndigits=1)
        print str(round((float(i)/len(data.ix[:,0]) * 100), ndigits=1)) + '%.  ' + str(current_score) + '% correct.'

    preds = Series(predictions)
    wl = Series(data.ix[:,'WL'])

    correct = float((preds == wl).sum())
    percent_correct = round(correct / (len(wl)) * 100, ndigits=2)

    print "Predictions were " + str(percent_correct) + "% correct."
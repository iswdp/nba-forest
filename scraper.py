import urllib, json

def scrape_nba():
    print 'Retrieving data.'
    team_ids = {'POR':1610612757, 'LAC':1610612746, 'HOU':1610612745, 'MIN':1610612750, 'OKC':1610612760, 'PHX':1610612756, 'MIA':1610612748, 'DAL':1610612742, 'SAS':1610612759, 'GSW':1610612744, 'DEN':1610612743, 'ATL':1610612737, 'LAL':1610612747, 'SAC':1610612758, 'DET':1610612765, 'WAS':1610612764, 'TOR':1610612761, 'PHI':1610612755, 'NOP':1610612740, 'IND':1610612754, 'BKN':1610612751, 'NYK':1610612752, 'CLE':1610612739, 'ORL':1610612753, 'MEM':1610612763, 'BOS':1610612738, 'CHA':1610612766, 'UTA':1610612762, 'MIL':1610612749, 'CHI':1610612741}
    team_data = {}

    for i in team_ids:
        htmltext = urllib.urlopen('http://stats.nba.com/stats/teamgamelog?Season=2013-14&SeasonType=Regular+Season&LeagueID=00&TeamID=' + str(team_ids[i]) + '&pageNo=1&rowsPerPage=25')
        json_file = json.load(htmltext)
        team_data[i] = json_file['resultSets'][0]['rowSet']
        print team_data[i][0]

    #headers = json_file['resultSets'][0]['headers'] #Uncomment to display json headers.
    json.dump(team_data, open('dictdata.txt','w'))

def scrape_aggre():
    print 'Retrieving data.'
    htmltext = urllib.urlopen('http://stats.nba.com/stats/leaguedashteamstats?Season=2013-14&AllStarSeason=2013-14&SeasonType=Regular+Season&LeagueID=00&MeasureType=Base&PerMode=PerGame&PlusMinus=N&PaceAdjust=N&Rank=N&Outcome=&Location=&Month=0&SeasonSegment=&DateFrom=&DateTo=&OpponentTeamID=0&VsConference=&VsDivision=&GameSegment=&Period=0&LastNGames=0&GameScope=&PlayerExperience=&PlayerPosition=&StarterBench=&pageNo=1&rowsPerPage=30&columnOrder=TEAM_NAME%2CGP%2CMIN%2CW%2CL%2CW_PCT%2CFGM%2CFGA%2CFG_PCT%2CFG3M%2CFG3A%2CFG3_PCT%2CFTM%2CFTA%2CFT_PCT%2COREB%2CDREB%2CREB%2CAST%2CTOV%2CSTL%2CBLK%2CBLKA%2CPF%2CPTS%2CPLUS_MINUS')
    json_file = json.load(htmltext)
    team_data = json_file['resultSets'][0]
    json.dump(team_data, open('aggre_data.txt', 'w'))
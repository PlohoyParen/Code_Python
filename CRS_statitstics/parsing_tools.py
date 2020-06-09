import datetime
import requests 
from bs4 import BeautifulSoup 
    
def parsing_string(list_of_strings):
    """
    Takes a list of <p> .. </p> dates and return a list of datetime format dates.
    List indeces correspond to number on entry on the website
    """
    total_list = []         # list containing all lists of entries
    current_list = []       # list containing one entry (one round of invitations)
    # basic cleaning 
    for entry in list_of_strings:
        mid_str = str(entry).replace('<p>','').replace('</p>','').replace('#','').replace(',', '')
        mid_str = mid_str.replace('<strong>','').replace('</strong>','').replace('<sup>th</sup>', '')

        # all invitation rounds end with this
        if "Tie-breaking rule" in mid_str:
            total_list.append(current_list)
            current_list = []
        else:
            current_list.append(mid_str)
    # remove all Non FSW programs
    fsw_list = []        
    for inv_round in total_list:
        for entry in inv_round:
            if 'No program specified' in entry:
                fsw_list.append(inv_round)
                break
    
    rank_list = []
    score_list = []
    date_list = [] 
    for inv_round in fsw_list:
        for entry in inv_round:
            # clean up for ranking
            if 'Rank required to be invited to apply' in entry:
                rank = 0
                for i in range(len(entry)):
                    # where int num begins
                    if (entry[i-1]+entry[i]) == ': ':
                        start = i+1
                    if (entry[i-1]+entry[i]) == 'or':
                    # where int num ends
                        end = i-2;
                        rank = int(entry[start:end])
#                print("rank: ", rank)
                rank_list.append(rank)

            # clean up for scores
            if 'CRS score of lowest-ranked candidate' in entry:
                score = 0
                for i in range(len(entry)):
                    # where int num begins
                    if (entry[i-1]+entry[i]) == ': ':
                        start = i+1
                        score = int(entry[start:])
#                print("score", score)
                score_list.append(score)
            # clean up for dates -> datetime
            if 'Date and time of round' in entry:
                entry = entry.replace('at', '')
                for i in range(len(entry)):
                    if entry[i] == ':':
                        entry = datetime.datetime.strptime(entry[i+2:], '%B %d %Y  %H:%M:%S %Z')
                        entry = datetime.date(entry.year, entry.month, entry.day)
                        break
                date_list.append(entry)
    # forming dict {'date':['lowest_score', 'num_accepted']}
    fsw_dict = {}
    for i in range(len(rank_list)):
        fsw_dict[date_list[i]] = [score_list[i], rank_list[i]]
    
    return fsw_dict


def old_crs_parser():
    URL = "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/submit-profile/rounds-invitations/results-previous.html"
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html5lib') 
    
    body = soup.find('div', attrs = {'class': 'mwsgeneric-base-html parbase section'})
    
    total_list = []         # list containing all lists of entries
    current_list = []       # list containing one entry (one round of invitations)
    for line in body.get_text().split("\n"):
        if '#' in line:
            total_list.append(current_list)
            current_list = []
            current_list.append(line)
        else:
            current_list.append(line)
    
    old_table_starts = 0
    for sub_list in total_list:    
        if '#76' in sub_list[0]:
            break
        old_table_starts += 1
    total_list = total_list[old_table_starts:]
    
    # remove all Non FSW programs
    fsw_list = []        
    for inv_round in total_list:
        for entry in inv_round:
            if 'No program specified' in entry:
                fsw_list.append(inv_round)
                break
    
    rank_list = []
    score_list = []
    date_list = [] 
    i =0
    fsw_list[18][12] = fsw_list[18][10]
    fsw_list[18][13] = fsw_list[18][11]
    fsw_list[19][12] = fsw_list[19][10]
    fsw_list[19][13] = fsw_list[19][11]
    
    fsw_list[57][12] = fsw_list[57][13]
    fsw_list[57][13] = fsw_list[57][14]
    fsw_list[38][12] = fsw_list[38][13]
    fsw_list[38][13] = fsw_list[38][14]
    
    for inv_round in fsw_list:
        rank_str = inv_round[12]
        rank_str = int(rank_str.replace(',', ''))
        rank_list.append(rank_str)
    
        score_str = inv_round[13]
        score_str = score_str.replace('\xa0points', '')
        score_str = int(score_str.replace(' points', '').strip())
        score_list.append(score_str)
        
        date_str = inv_round[0]
        date_str = date_str.replace(',', '')
        for i in range(len(date_str)):
            if date_str[i] == '–':
                date_str = datetime.datetime.strptime(date_str[i+2:], '%B %d %Y')
                break
        date_list.append(date_str)
    
    # forming dict {'date':['lowest_score', 'num_accepted']}
    fsw_dict = {}
    for i in range(len(rank_list)):
        fsw_dict[date_list[i]] = [score_list[i], rank_list[i]]
    
    return fsw_dict
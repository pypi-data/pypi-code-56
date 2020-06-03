""" 
Supplementary functions for TBML (bettingmodels) app

"""

import pandas as pd
import datetime
from bs4 import BeautifulSoup
import requests
import numpy as np

def _is_player_name(tag):
    if tag.name=="h3":
        return True
    return False

## Check if TE tag on player page contains player's nationality

def _is_player_country(tag):
    if tag.has_attr("class"):
        if tag["class"]==["date"]:
            if list(tag.descendants)[0][:7]=="Country":
                return True
    return False

## Check if TE tag on player page contains player's birth date

def _is_player_birthdate(tag):
    if tag.has_attr("class"):
        if tag["class"]==["date"]:
            if list(tag.descendants)[0][:4]=="Born":
                return True
    return False

## Check if TE tag on player page contains player's gender

def _is_player_gender(tag):
    if tag.has_attr("class"):
        if tag["class"]==["date"]:
            if list(tag.descendants)[0][:3]=="Sex":
                return True
    return False

## Check if TE tag on player page contains player's preferred hand

def _is_player_handed(tag):
    if tag.has_attr("class"):
        if tag["class"]==["date"]:
            if list(tag.descendants)[0][:5]=="Plays":
                return True
    return False

## Check if TE tag on results page contains tournament name

def _is_tourney(tag):
    if tag.has_attr("class") and tag.has_attr("colspan"):
        if tag["colspan"]=="2":
            return True
    return False

## Check if TE tag on results page contains match time

def _is_match_time(tag):
    if tag.has_attr("class"):
        if tag["class"]==['first', 'time']:
            return True
    return False

## Check if TE tag on results page contains link to match details

def _is_link_matchdetails(tag):
    if not tag.has_attr("class") and tag.has_attr("rowspan"):
        if tag["rowspan"]=="2":
            return True
    return False

## Check if TE tag on results page contains player ID

def _is_player(tag):
    if tag.has_attr("class") and not tag.has_attr("colspan"):
        if tag["class"]==['t-name']:
            return True
    return False

## Check if TE tag on results page contains match result

def _is_result(tag):
    if tag.has_attr("class"):
        if tag["class"]==['result']:
            return True
    return False

## Check if TE tag on results page contains match score

def _is_score(tag):
    if tag.has_attr("class"):
        if tag["class"]==['score']:
            return True
    return False

   
## Switch Player 1 and Player 2 data in Matches data frame including
## corresponding scores
## Input: data frame containing matches
## Output: data frame containing permuted matches
    
def _permute_matches(df):
    df['permute']=np.random.choice([True,False], df.shape[0])
    rows_to_permute=df[df['permute']==True]
    counter=0
    for index in list(rows_to_permute.index.values):
        df.loc[index,['Player1','Player2']] \
        = df.loc[index,['Player2','Player1']].values
        df.loc[index,['SetsPlayer1','SetsPlayer2']] \
        = df.loc[index,['SetsPlayer2','SetsPlayer1']].values
        df.loc[index,['Set1Player1','Set1Player2']] \
        = df.loc[index,['Set1Player2','Set1Player1']].values
        df.loc[index,['Set2Player1','Set2Player2']] \
        = df.loc[index,['Set2Player2','Set2Player1']].values
        df.loc[index,['Set3Player1','Set3Player2']] \
        = df.loc[index,['Set3Player2','Set3Player1']].values
        df.loc[index,['Set4Player1','Set4Player2']] \
        = df.loc[index,['Set4Player2','Set4Player1']].values
        df.loc[index,['Set5Player1','Set5Player2']] \
        = df.loc[index,['Set5Player2','Set5Player1']].values
        df.loc[index,['Result']]=-df.loc[index,['Result']].values+3
        df.loc[index,['Retired']]=df.loc[index,['Retired']].values/2
        counter+=1
        print(str(counter)+" of "+str(rows_to_permute.shape[0])+" matches permuted")
    return df

## Process matches by calculating games, tiebreaks, result and retired values
    
def processing1(df_matches):
    
    # define tournaments with best-of-five
    fivesetters=["australian-open-atp-single",
                 "french-open-atp-single",
                 "wimbledon-atp-single",
                 "us-open-atp-single",
                 "davis-cup-atp-single",
                 "olympics-london-atp-single",
                 "olympics-beijing-atp-single",
                 "olympics-athens-atp-single",
                 "olympics-rio-de-janeiro-atp-single"]
    
    # determine Result and Retired values
    df_matches['Result']=-((df_matches['SetsPlayer1']>df_matches['SetsPlayer2'])*1-2)
    df_matches['Retired']=np.where(df_matches[['SetsPlayer1','SetsPlayer2']].max(axis=1)<2,2,0)
    
    # permute matches
    df_matches = _permute_matches(df_matches)
    df_matches = df_matches.drop("permute",axis=1)    
    print ("Permutation completed")


    # calculate GamesOverallPlayerX    
    df_matches['GamesOverallPlayer1']=df_matches[['Set1Player1',
              'Set2Player1','Set3Player1','Set4Player1',
              'Set5Player1']].sum(axis=1)
    df_matches['GamesOverallPlayer2']=df_matches[['Set1Player2',
              'Set2Player2','Set3Player2','Set4Player2',
              'Set5Player2']].sum(axis=1)
    
    # calculate TiebreaksPlayerX
    df_matches['TiebreaksPlayer1']=np.where(
            np.logical_and(
                    df_matches['Set1Player1']==7,
                    df_matches['Set1Player2']==6),1,0) \
            + np.where(np.logical_and(
                    df_matches['Set2Player1']==7,
                    df_matches['Set2Player2']==6),1,0) \
                    + np.where(
                            np.logical_and(
                                    df_matches['Set3Player1']==7,
                                    df_matches['Set3Player2']==6),1,0) \
                            + np.where(
                                    np.logical_and(
                                            df_matches['Set4Player1']==7,
                                            df_matches['Set4Player2']==6),1,0) \
                                    + np.where(
                                            np.logical_and(
                                                    df_matches['Set5Player1']==7,
                                                    df_matches['Set5Player2']==6),1,0)
    df_matches['TiebreaksPlayer2']=np.where(
            np.logical_and(
                    df_matches['Set1Player1']==6,
                    df_matches['Set1Player2']==7),1,0) \
            + np.where(np.logical_and(
                    df_matches['Set2Player1']==6,
                    df_matches['Set2Player2']==7),1,0) \
                    + np.where(
                            np.logical_and(
                                    df_matches['Set3Player1']==6,
                                    df_matches['Set3Player2']==7),1,0) \
                            + np.where(
                                    np.logical_and(
                                            df_matches['Set4Player1']==6,
                                            df_matches['Set4Player2']==7),1,0) \
                                    + np.where(
                                            np.logical_and(
                                                    df_matches['Set5Player1']==6,
                                                    df_matches['Set5Player2']==7),1,0)
    
    # calculate GamesPlayerX by subtracting Tiebreaks from GamesOverall
    df_matches['GamesPlayer1']=df_matches['GamesOverallPlayer1'] \
    - df_matches['TiebreaksPlayer1']
    df_matches['GamesPlayer2']=df_matches['GamesOverallPlayer2'] \
    - df_matches['TiebreaksPlayer2']
    
    print("Games and tiebreaks completed")
    
    # handle tiebreak tens
    # identify
    df_matches_tbtens=df_matches[
            df_matches['Retired']==0][
                    (((df_matches['Set3Player1']==10) \
                      | (df_matches['Set3Player2']==10)) \
    | (df_matches['Set3Player1']>10) \
    & (df_matches['Set3Player1'] \
       - df_matches['Set3Player2']==2)) \
    | ((df_matches['Set3Player2']>10) \
       & (df_matches['Set3Player2']-df_matches['Set3Player1']==2))]
    
    # separate from "normal" matches
    df_matches_tbtens=df_matches_tbtens[~df_matches_tbtens['Tourney'].isin(
            fivesetters)]
    
    df_matches_rest=df_matches[
            ~df_matches.index.isin(df_matches_tbtens.index.values)]
    
    print (str(df_matches_tbtens.shape[0])+" matches with tiebreak tens found")
    
    # iterate and modify GamesOverall, Games and Tiebreaks
    for index,row in df_matches_tbtens.iterrows():
        
        currentmatch=index
        print ("Processing match "+str(currentmatch))
        
        df_matches_tbtens.loc[currentmatch,'GamesPlayer1'] \
        =df_matches_tbtens.loc[currentmatch,'GamesPlayer1'] \
        - df_matches_tbtens.loc[currentmatch,'Set3Player1']
        
        df_matches_tbtens.loc[currentmatch,'GamesPlayer2'] \
        =df_matches_tbtens.loc[currentmatch,'GamesPlayer2'] \
        - df_matches_tbtens.loc[currentmatch,'Set3Player2']
        
        df_matches_tbtens.loc[currentmatch,'GamesOverallPlayer1'] \
        =df_matches_tbtens.loc[currentmatch,'GamesOverallPlayer1'] \
        - df_matches_tbtens.loc[currentmatch,'Set3Player1']
        
        df_matches_tbtens.loc[currentmatch,'GamesOverallPlayer2'] \
        =df_matches_tbtens.loc[currentmatch,'GamesOverallPlayer2'] \
        - df_matches_tbtens.loc[currentmatch,'Set3Player2']
    
        
        df_matches_tbtens.loc[currentmatch,'TiebreaksPlayer1'] \
        = df_matches_tbtens.loc[currentmatch,'TiebreaksPlayer1'] \
        + (df_matches_tbtens.loc[currentmatch,'Set3Player1'] \
         >df_matches_tbtens.loc[currentmatch,'Set3Player2'])
        
        df_matches_tbtens.loc[currentmatch,'TiebreaksPlayer2'] \
        = df_matches_tbtens.loc[currentmatch,'TiebreaksPlayer2'] \
        + (df_matches_tbtens.loc[currentmatch,'Set3Player1'] \
         < df_matches_tbtens.loc[currentmatch,'Set3Player2'])
    
        df_matches_tbtens.loc[currentmatch,'GamesOverallPlayer1'] \
        = df_matches_tbtens.loc[currentmatch,'GamesOverallPlayer1'] \
        + (df_matches_tbtens.loc[currentmatch,'Set3Player1'] \
         >df_matches_tbtens.loc[currentmatch,'Set3Player2'])
        
        df_matches_tbtens.loc[currentmatch,'GamesOverallPlayer2'] \
        = df_matches_tbtens.loc[currentmatch,'GamesOverallPlayer2'] \
        + (df_matches_tbtens.loc[currentmatch,'Set3Player1'] \
         < df_matches_tbtens.loc[currentmatch,'Set3Player2'])
    
    # concatenate back    
    df_matches=pd.concat([df_matches_rest,df_matches_tbtens])
    df_matches=df_matches.sort_values(
            ['DateTime'],ascending=[True])
    
    print("Matches with tiebreak tens processed")
    
    return df_matches    

## Download player data
## Input: TE player ID
## Output: Dataframe of length 1 containing player data

def download_player(player_id):
    
    # find webpage with player info and convert to BeautifulSoup                                                
    url="http://www.tennisexplorer.com/player/"+player_id
    urlcontents = requests.get(url).text
    soup = BeautifulSoup(urlcontents, "lxml")

    # create dictionary for player data
    current_player={"id_te":player_id}

    # find <td> tag with player data in BeautifulSoup
    # fill current_player with player data 
    playerData=list(soup.find_all(
        "tbody")[0].descendants)[1].find_all("td")[1]

    for tag in playerData:
        if _is_player_name(tag):
            current_player["name"]=list(tag.descendants)[0]

        if _is_player_country(tag):
            current_player["country"]=list(tag.descendants)[0][9:]

        if _is_player_birthdate(tag):
            current_player["birthdate"]=datetime.datetime.strptime(
                list(tag.descendants)[0][6:].replace(" ",""),
                "%d.%m.%Y").date()

        if _is_player_gender(tag):
            current_player["gender"]=list(tag.descendants)[0][5:]

        if _is_player_handed(tag):
            current_player["handed"]=list(tag.descendants)[0][7:]

    if not "country" in current_player:
        current_player["country"]=None

    if not "birthdate" in current_player:
        current_player["birthdate"]=None

    if not "handed" in current_player:
        current_player["handed"]=None

    # convert current_player to Pandas dataframe
    df_currentplayer=pd.DataFrame({'PlayerID':current_player["id_te"],
                                   'Name':current_player["name"],
                                   'Country':current_player["country"],
                                   'Birthdate':current_player["birthdate"],
                                   'Gender':current_player["gender"],
                                   'Handed':current_player["handed"]},
                index=['PlayerID'])
    df_currentplayer=df_currentplayer.set_index(['PlayerID'])
    
    print ("Player "+player_id+" added")
    
    return df_currentplayer

## Download tourney data
## Input: TE tourney ID
## Output: Dataframe of length 1 containing player data

def download_tourney(tourney_id,results_type,year):
    
    # convert ATP/WTA to correct url
    if results_type == "atp-single":
        results_type_url="atp-men"
    elif results_type == "wta-single":
        results_type_url = "wta-women"
    
    # find webpage with tourney info and convert to BeautifulSoup 
    url="http://www.tennisexplorer.com/" \
    + tourney_id + "/" \
    + str(year) + "/" \
    + results_type_url 
    
    urlcontents = requests.get(url).text
    tourney_id_composed=tourney_id+"-"+results_type
    
    # catch tournaments without data (e.g. Futures)
    if "Tournament does not exist" in urlcontents:
        df_currenttourney=pd.DataFrame({'TourneyIDComposed':tourney_id_composed,
                                        'TourneyName':tourney_id,
                                        'Gender':results_type_url[4:].replace('e','a'),
                                        'Country':None,
                                        'Surface':None},
        index=['TourneyIDComposed'])
        df_currenttourney=df_currenttourney.set_index(['TourneyIDComposed'])
        print("Tourney "+tourney_id_composed+" added")
        return(df_currenttourney)
    
    soup = BeautifulSoup(urlcontents, "lxml")
    
    # create dictionary for tourney data    
    current_tourney={"id_te":tourney_id_composed,
                     "gender":results_type_url[4:].replace('e','a')}
    
    # find tags with tourney data in BeautifulSoup
    # fill current_tourney with tourney data 
    
    tourney_data1=list(soup.find_all("h1")[0].descendants)[0]
    current_tourney['tourney_name']=tourney_data1[
            :tourney_data1.index("(")-6]
    current_tourney['country']=tourney_data1[
            tourney_data1.index("(")+1:-1]
    
    tourney_data2=list(soup.find_all(
            "div", {'class':'box boxBasic lGray'})[1].descendants)[0]
    current_tourney['surface']=tourney_data2.split(',')[-2][1:]
    
    # convert current_tourney to Pandas dataframe
    df_currenttourney=pd.DataFrame({'TourneyIDComposed':current_tourney["id_te"],
                                    'TourneyName':current_tourney["tourney_name"],
                                    'Gender':current_tourney["gender"],
                                    'Country':current_tourney["country"],
                                    'Surface':current_tourney["surface"]},
    index=['TourneyIDComposed'])
    df_currenttourney=df_currenttourney.set_index(['TourneyIDComposed'])
    print("Tourney "+current_tourney["id_te"]+" added")
    
    return df_currenttourney

## Downloads match results for range of dates
## returns pandas dataframe with match results, updated players and tourneys 
## dataframe
    
## start_date: datetime.datetime object containing first date in date range
## end_date: datetime.datetime object containing last date in date range
## updatePlayers: boolean whether new players should be downloaded
## **kwargs (match_ids, player_ids, tourney_ids): ID lists for matches, 
## players and tourneys in the database  

def download_matches(start_date,
                     end_date,
                     results_type,
                     **kwargs):
    
    # Create list of all dates between start_date and end_date
    
    date_list = [start_date + datetime.timedelta(days=x)
                 for x in range(0, (end_date-start_date).days+1)]

    # Create empty data frames for new results, players, tourneys

    columns_results=['MatchID',
                     'DateTime',
                     'Tourney',
                     'Player1',
                     'Player2',
                     'SetsPlayer1',
                     'SetsPlayer2',
                     'Set1Player1',
                     'Set2Player1',
                     'Set3Player1',
                     'Set4Player1',
                     'Set5Player1',
                     'Set1Player2',
                     'Set2Player2',
                     'Set3Player2',
                     'Set4Player2',
                     'Set5Player2',
                     'finished']
    df_results_new=pd.DataFrame(columns=columns_results)    

    if 'player_ids' in kwargs:
        columns_players=['PlayerID',
                         'Name',
                         'Country',
                         'Birthdate',
                         'Gender',
                         'Handed']
        df_players_new=pd.DataFrame(columns=columns_players)
        df_players_new=df_players_new.set_index(['PlayerID'])

    if 'tourney_ids' in kwargs:
        columns_tourneys=['TourneyIDComposed',
                          'TourneyName',
                          'Gender',
                          'Country',
                          'Surface']
        df_tourneys_new=pd.DataFrame(columns=columns_tourneys)
        df_tourneys_new=df_tourneys_new.set_index(['TourneyIDComposed'])

    # Iterate through date list

    for currentdate in date_list:
        print("Starting "+currentdate.strftime("%Y-%m-%d"))
        
        # Create URL, open TE page, create BS object with page contents
        
        url="http://www.tennisexplorer.com/results/?type=" + \
             results_type + \
             "&year=" + str(currentdate.year) + \
             "&month=" + str(currentdate.month) + \
             "&day="+str(currentdate.day)
        urlcontents = requests.get(url).text
        soup = BeautifulSoup(urlcontents, "lxml")

        # Create empty dictionaries/lists for match/tourney details

        current_tourney={}
        current_match={}
        current_match["score_sets"]=[]
        current_match["scores_p1"]=[]
        current_match["scores_p2"]=[]

        # Find results table and all results tags

        resultsTable = soup.find("table", {"class":"result"})
        results_tags = resultsTable.find_all("td")

        # Define variables to open/close match, Player 1/2 scores
        # These variables delineate between single matches/players

        match_open=False
        first_player_open=False
        second_player_open=False
        
        # Iterate through tags in results table

        for tag in results_tags:
            
            # Check if tag contains tourney details and fill current_tourney
            # else branch catches tourneys without hyperlink (<a> tag, e.g. 
            # Futures events)
            
            if _is_tourney(tag):
                if tag.find("a"):
                    current_tourney["url"]=list(tag.descendants)[0]["href"]
                    tid=current_tourney["url"][1:]
                    current_tourney["id"]= tid[:tid.index("/")]                                                                          
                    current_tourney["name"]=list(tag.descendants)[-1]
                else:
                    current_tourney["url"]=None
                    current_tourney["name"]=list(tag.descendants)[-1]
                    current_tourney["id"]=current_tourney["name"].replace(" ","-").lower()
                
                
                current_tourney_id_composed=current_tourney["id"] \
                + "-" + results_type
                currentyear=currentdate.year
                
                # Check if tourney_id exists in database, add to new
                # tourney data frame if missing
                
                if 'tourney_ids' in kwargs:
                    if ((current_tourney_id_composed \
                        not in kwargs['tourney_ids']) \
                        and (current_tourney_id_composed \
                        not in df_tourneys_new.index.unique())):
                        df_t=download_tourney(current_tourney["id"],
                                              results_type,
                                              currentyear)
                        df_tourneys_new=pd.concat([df_tourneys_new, df_t])

            # Check if tag contains match time

            if _is_match_time(tag):

                # Open match and Player 1 with match time tag
                
                match_open=True
                first_player_open=True
                
                # Fill current_match dictionary with current tourney and
                # date/time (23:59 if time is missing)

                current_match["tourney"]=current_tourney
                try:
                    current_match["datetime"]=str(currentdate.year)+"-"\
                                              +str(currentdate.month)+"-"\
                                              +str(currentdate.day)+" "\
                                              +list(tag.descendants)[0][:2]+":"\
                                              +list(tag.descendants)[0][-2:]+":"\
                                              +"0"
                except ValueError:
                    current_match["datetime"]=str(currentdate.year)+"-"\
                                              +str(currentdate.month)+"-"\
                                              +str(currentdate.day)+" "\
                                              +"23:59:00"

            # Exctract match details URL and match ID

            if match_open and _is_link_matchdetails(tag):
                current_match["url"]=list(tag.descendants)[0]["href"]
                current_match["id_te"]=list(tag.descendants)[0]["href"][18:]
                
            if match_open and _is_player(tag):
                
                # Extract Player 1 details
                
                if first_player_open:
                    try:
                        current_match["p1"]={
                            "name":list(tag.descendants)[1],
                            "url":list(tag.descendants)[0]["href"],
                            "id":list(tag.descendants)[0]["href"][8:-1]}
                    except IndexError:
                        current_match["p1"]={
                            "name":list(tag.descendants)[0],
                            "url":None,
                            "id":None}
                
                # Extract Player 2 details
                
                elif second_player_open:
                    try:
                        current_match["p2"]={
                            "name":list(tag.descendants)[1],
                            "url":list(tag.descendants)[0]["href"],
                            "id":list(tag.descendants)[0]["href"][8:-1]}
                    except IndexError:
                        current_match["p2"]={
                            "name":list(tag.descendants)[0],
                            "url":None,
                            "id":None}

            # Extract match result in sets
                
            if match_open and _is_result(tag):
                if list(tag.descendants)[0]=="\xa0":
                    current_match["score_sets"].append(None)
                else:
                    current_match["score_sets"].append(int(list(tag.descendants)[0]))

            # Extract set scores

            if match_open and _is_score(tag):
                
                # Extract set scores for Player 1
                
                if first_player_open:
                    if list(tag.descendants)[0]=="\xa0":
                        current_match["scores_p1"].append(None)
                    else:
                        current_match["scores_p1"].append(int(list(tag.descendants)[0]))
                
                # Extract set scores for Player 2
                
                elif second_player_open:
                    if list(tag.descendants)[0]=="\xa0":
                        current_match["scores_p2"].append(None)
                    else:
                        current_match["scores_p2"].append(int(list(tag.descendants)[0]))

            # Open Player 2 when 5 set score tags for Player 1 and fewer than 5
            # set score tags for Player 2 are iterated through

            if match_open and (
                len(current_match["scores_p1"])>=5 and len(current_match["scores_p2"])<5):
                first_player_open=False
                second_player_open=True

            # Close Player 2 and match when 5 sets for Player 2 are iterated
            # through

            if match_open and (
                len(current_match["scores_p1"])>=5 and len(current_match["scores_p2"])>=5):
                second_player_open=False
                match_open=False
                current_match["finished"]=1

                # Add Player 1 to new players data frame if Player 1 not in 
                # database

                if 'player_ids' in kwargs:
                    if ((current_match["p1"]["id"] \
                        not in kwargs['player_ids']) \
                        and (current_match["p1"]["id"] \
                        not in df_players_new.index.unique()) \
                             and current_match["p1"]["id"]):
                        try:
                            df_p1=download_player(current_match["p1"]["id"])
                            df_players_new=pd.concat([df_players_new, df_p1])
                        except IndexError:
                            current_match["p1"]["id"]=None

                # Add Player 2 to new players data frame if Player 2 not in 
                # database

                if 'player_ids' in kwargs:
                    if ((current_match["p2"]["id"] \
                        not in kwargs['player_ids']) \
                        and (current_match["p2"]["id"] \
                        not in df_players_new.index.unique()) \
                        and current_match["p2"]["id"]):
                        try:
                            df_p2=download_player(current_match["p2"]["id"])
                            df_players_new=pd.concat([df_players_new, df_p2])
                        except IndexError:
                            current_match["p2"]["id"]=None

                # Create data frame with new match if match not in old matches
                # data frame and append to new matches data frame, growing it
                # by 1

                df_currentmatch=pd.DataFrame({
                        'MatchID':current_match["id_te"],
                        'DateTime':current_match["datetime"],
                        'Tourney':current_tourney_id_composed,
                        'Player1':current_match["p1"]["id"],
                        'Player2':current_match["p2"]["id"],
                        'SetsPlayer1':current_match["score_sets"][0],
                        'SetsPlayer2':current_match["score_sets"][1],
                        'Set1Player1':current_match["scores_p1"][0],
                        'Set2Player1':current_match["scores_p1"][1],
                        'Set3Player1':current_match["scores_p1"][2],
                        'Set4Player1':current_match["scores_p1"][3],
                        'Set5Player1':current_match["scores_p1"][4],
                        'Set1Player2':current_match["scores_p2"][0],
                        'Set2Player2':current_match["scores_p2"][1],
                        'Set3Player2':current_match["scores_p2"][2],
                        'Set4Player2':current_match["scores_p2"][3],
                        'Set5Player2':current_match["scores_p2"][4],
                        'finished':current_match["finished"]},
                                                 index=['MatchID'])
                df_results_new=pd.concat([df_results_new,df_currentmatch])
                
                # Reset current_match dictionary
                
                current_match={}
                current_match["score_sets"]=[]
                current_match["scores_p1"]=[]
                current_match["scores_p2"]=[]

        print(currentdate.strftime("%Y-%m-%d")+" completed")
        
    # Set index of new data frames
    
    df_results_new=df_results_new.set_index("MatchID")

    # Return different set of data frames depending passed kwargs

    if (('player_ids' in kwargs) and ('tourney_ids' not in kwargs)):
        return df_results_new, df_players_new
    
    if (('tourney_ids' in kwargs) and ('player_ids' not in kwargs)):
        return df_results_new, df_tourneys_new
    
    if (('player_ids' in kwargs) and ('tourney_ids' in kwargs)):
        return df_results_new, df_players_new, df_tourneys_new

    return df_results_new

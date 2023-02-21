# coding: utf8

import pandas
import json
import os
import time
from datetime import datetime
from datetime import timedelta
from fpdf import FPDF
from classes.Statistics import Statistics
import glob

def checkAllSameInList(lst):
    """
    method to check if every element in an array are the same
    used for the queues (if all queue types are the same then, single queue type)

    :param list lst: list which need to be checked in order to say if all elements are the same
    """
    # if list is empty or contains only one element
    # returns true
    if (len(lst)<=1):
        return True
    
    # first element that we
    elt = lst[0]
    # boolean returned that says if a elements in a list are all the same
    res = True 
    # Comparing each element with first item
    for item in lst:
        if elt != item:
            # first occurence of false condition, no need to go further
            res = False
            break

    return res


def isFileOlderThanOneDay(file): 
    """
    Returns False or True depending on if the file modification given in argument is older than one day.

    :param str file: The path of the file
    """
    file_time = os.path.getmtime(file) 
    # Check against 24 hours 
    return ((time.time() - file_time) / 3600 > 24)

def jsonObjectToCSV(data: list, region: str, summonerName: str = None, rankLeague: str = None, queueType: str = None, dataType: str = None, gameId: str = None):
    """
    Creates a CSV file with data sent in region folder of the data folder.

    :param list data: The array containing data to store in the CSV
    :param str region: The region that data comes from
    :param summonerName: The summoner name
    :type summonerName: str or None
    :param rankLeague: The rank league data come from (challenger, grandmaster, master)
    :type rankLeague: str or None
    :param queueType: The type of queue (RANKED_FLEX_SR or RANKED_SOLO_5x5)
    :type queueType: str or None
    :param dataType: The data type that the CSV holds
    :type dataType: str or None
    :param gameId: The id of the game
    :type gameId: str or None
    """
    # Path where the files will be stored (i.e the folder corresponding to the game's region in the data folder )
    if (gameId == None):
        fileName = "./data/" + region + "/" + region + "_" + rankLeague + "/" + dataType + "/" + region + "_" + dataType
    elif (rankLeague == None and summonerName != None and queueType != None):
        if queueType == "":
            fileName = "./data/" + region + "/" + region  + "_" + summonerName + "/" + queueType + "/" + dataType + "/" + gameId + "_" + dataType
        else :
            fileName = "./data/" + region + "/" + region  + "_" + summonerName + "/" + queueType + "/" + dataType + "/" + gameId + "_" + dataType
    else:
        fileName = "./data/" + region + "/" + region  + "_" + rankLeague + "/" + dataType + "/"+ gameId + "_" + dataType

    # Creates the directory if it doesn't exist
    os.makedirs(os.path.dirname(fileName + ".json"), exist_ok = True)

    # Converts objects in a json string
    jsonString = json.dumps(data, indent = 4)
    # Store the json string in a file
    with open(fileName + ".json", "w+") as outfile:
        outfile.write(jsonString)

    # Read the json file previously created
    df = pandas.read_json(fileName + ".json")
    # Convert the json into a CSV
    df.to_csv(fileName + ".csv", index = None)
    # Delete the json file
    os.remove(fileName + ".json")

def csvToCommonPdfReport(region: str, rankLeague: str, summonersNames: list, queueType: list, gameIds: list, roles: list=[], teamSide: list=[], championsPlayedByEachPlayer: list = [], teamSideFilter: str = None):
    """
    Creates a pdf file for common team reports with data sent in region folder of the data folder.

    :param str region: The region of the CSVs 
    :param str rankLeague: The rank league (challenger, grandmaster or master)
    :param str summonersNames: The summoners names that played a game in common
    :param list queueType: Array of type of queue (RANKED_FLEX_SR or RANKED_SOLO_5x5)
    :param list gameIds: Array of game id
    :param roles: The roles of the summoners that played a game in common
    :type roles: list or None 
    :param list teamSide: Array of team side of games (Red or blue)
    :param list championsPlayedByEachPlayer: Array of champions arrays filtered
    :param str teamSideFilter: The team side filtered (Red, blue or both)
    """

    if (rankLeague == None and len(summonersNames)!=0 and queueType != None):

        fileName=""
        gamesPath = []
        pathToParticipant = ""

        match(teamSideFilter):
            case "Blue side":
                teamSideFilter="BLUE_TEAM"
            case "Red side":
                teamSideFilter="RED_TEAM"

        summonersFileName = ""

        # Concatenate the summoner names to correspond to the path
        for i in range(len(summonersNames)):
            summonersFileName += summonersNames[i] + "_"
        summonersFileName = summonersFileName[:-1]

        # Loop through all the games retrieved
        for i in range(len(gameIds)):
            # Path of the csv files
            pathToParticipant='data/'+region+'/'+region+'_'+summonersFileName + "/"+queueType[i]+"/participant"

            filePath = pathToParticipant+'/'+gameIds[i]+'_participant.csv'
            # Store the game path in an array
            if not(filePath in gamesPath) :
                gamesPath.append(filePath)

        # name of the pdf common report file
        fileName = region+"_"+queueType[0]+"_"

        for i in range(len(summonersNames)):
            if(roles[i] != None):
                fileName += roles[i]+"_"
            fileName += summonersNames[i]+"_"
        fileName=fileName[:-1]

        # title in the pdf file
        title = "Report of: "

        # we keep only the games that are IN COMMON + that respect all filters of every players checked
        commonGamesRespectingFilters=[]

        # Loop through all summoners
        for i in range(len(summonersNames)):

            title += summonersNames[i]
            if(roles[i] != None):
                title += " ("+roles[i]+") "

            stat = Statistics(region,summonersNames[i],None)

            for j in range(len(gameIds)):
                gameRespectFilters=False
                if len(championsPlayedByEachPlayer[i]) !=0 :
                    for k in range(len(championsPlayedByEachPlayer[i])):
                        gameRespectFilters = stat.doesGameRespectFilters(gameIds[j],roles[i],gamesPath[j],championsPlayedByEachPlayer[i][k],teamSide[j],teamSideFilter)
                        if gameRespectFilters :
                            break
                else :
                    gameRespectFilters = stat.doesGameRespectFilters(gameIds[j],roles[i],gamesPath[j],None,teamSide[j],teamSideFilter)

                if (gameRespectFilters):
                    # correct filters for summonersNames[i] in gameIds[j]
                    commonGamesRespectingFilters.append(gameIds[j])
                # else gameIds[j] removed

        # used for commonGamesRespectingFilters array
        # when a game id appears nth (player checked) times
        # then it means that this game is in common (every players were in this game)
        def check_number_of_occurences_value(lst, val):
            counter = 0
            for item in lst :
                if item==val :
                    counter=counter+1
            return counter

        list1 =[]
        for i in range(len(commonGamesRespectingFilters)):
            idOfGame = commonGamesRespectingFilters[i]
            # if game id appears (player checked) times
            # then it means that this game is in common (every players were in this game)
            if check_number_of_occurences_value(commonGamesRespectingFilters,idOfGame)==len(summonersNames) :
                list1.append(idOfGame)
        # removing duplicates
        list2 = []
        for item in list1:
            if item not in list2:
                list2.append(item)
        commonGamesRespectingFilters=list2

        # altering team side array because some of the game might not be in common (if team report)(so no longer present)
        teamSide2=[]
        for i in range(len(gameIds)) :
            if gameIds[i] in commonGamesRespectingFilters :
                teamSide2.append(teamSide[i])
        teamSide=teamSide2

        gamesPath=[]
        # Loop through all the games in common, 
        # to redefine gamepath with only the paths of the games that respected filters
        for i in range(len(commonGamesRespectingFilters)):
            # Path of the csv files
            pathToParticipant='data/'+region+'/'+region+'_'+summonersFileName + "/"+queueType[i]+"/participant"

            filePath = pathToParticipant+'/'+commonGamesRespectingFilters[i]+'_participant.csv'
            # Store the game path in an array
            if not(filePath in gamesPath) :
                gamesPath.append(filePath)

        # Loop through all summoners again 
        # (because commonGamesRespectingFilters with its final values)
        for i in range(len(summonersNames)):
            stat = Statistics(region,summonersNames[i],None)
            # if(len(commonGamesRespectingFilters)>1):
            # Generate the global graph
            stat.csStatsOfGames(commonGamesRespectingFilters, roles[i], gamesPath, championsPlayedByEachPlayer[i], teamSide, teamSideFilter)

        # array to store the titles of each graph in order to use them for image legends after
        statsTitlesArray=[]
        for i in range(len(summonersNames)):
            stat = Statistics(region,summonersNames[i],None)
            # if all games used are incorrect, no graph produced
            numberOfIncorrectGames=0
            for j in range(len(commonGamesRespectingFilters)):

                # creates foo(i).png
                gameRespectFilters=False
                if len(championsPlayedByEachPlayer[i]) !=0 :
                    for k in range(len(championsPlayedByEachPlayer[i])):
                        gameRespectFilters = stat.csStatsOfOneGame(commonGamesRespectingFilters[j],roles[i],gamesPath[j],championsPlayedByEachPlayer[i][k],teamSide[j],teamSideFilter)
                        if gameRespectFilters :
                            break
                else :
                    gameRespectFilters = stat.csStatsOfOneGame(commonGamesRespectingFilters[j],roles[i],gamesPath[j],None,teamSide[j],teamSideFilter)

                if (gameRespectFilters):
                    specificGameStatsLabel = summonersNames[i]
                    # If the role filter is set to fill, get the correct role for the current game to show it
                    if (roles[i] == "FILL"):
                        ourSummonerRole = stat.getOurSummonerRole(gamesPath[j])
                        specificGameStatsLabel += " (" + ourSummonerRole + "):\n"
                    else:
                        specificGameStatsLabel += " (" + roles[i] + "):\n"

                    # Get summoners champions to put in the label
                    ourSummonerChampName = stat.getOurSummonerChampionName(gamesPath[j])
                    ourSummonerOpponentChampName = stat.getOurSummonerOpponentChampionName(gamesPath[j])

                    specificGameStatsLabel += "Creep score comparison between " + ourSummonerChampName + " and " + ourSummonerOpponentChampName
                    if (queueType[j] == "RANKED_SOLO_5x5"):
                        specificGameStatsLabel += "\n(Ranked Solo/Duo)"
                    if (queueType[j] == "RANKED_FLEX_SR"):
                        specificGameStatsLabel += "\n(Ranked Flex)"
                    statsTitlesArray.append(specificGameStatsLabel)
                else :
                    numberOfIncorrectGames = numberOfIncorrectGames+1

        # if all games are incorrect, then no report produced, otherwise, report produced
        if numberOfIncorrectGames!=len(commonGamesRespectingFilters) :

            if(commonGamesRespectingFilters != None and len(commonGamesRespectingFilters) != 0):
                title+="\n"
                title += str(len(commonGamesRespectingFilters)-numberOfIncorrectGames)
                if len(commonGamesRespectingFilters)-numberOfIncorrectGames!=1 :
                    title+= " games "
                else :
                    title+= " game "
                title+="("+ region + ")"
            title=title.encode('latin-1', 'ignore').decode('latin-1')

            pdf=templateOfPdfReport(title)

            # globals stats of summoners images
            for i in range(len(summonersNames)):
                # if there are no global stats graph (no direct opponent case) then no image created
                # images are created one by one by order, so if global3 does not exist, the next one won't to
                if not(os.path.exists("./data/temp/global"+str(i+1)+".png")) :
                    break
                pdf.add_page()
                pdf.image("./data/temp/global"+str(i+1)+".png", x = (pdf.w - 175) / 2, w = 175, h = 175)
                globalStatsName="Global creep score between " + summonersNames[i] + " and his opponents"
                pdf.multi_cell(0, 8, globalStatsName.encode('latin-1', 'ignore').decode('latin-1'), align="C")

            # stats for each game of each summoner images
            counter = 0
            for i in range(len(summonersNames)):
                for j in range(len(commonGamesRespectingFilters)):
                    if not(os.path.exists("./data/temp/foo"+str(counter+1)+".png")) :
                        break
                    pdf.add_page()
                    pdf.image("./data/temp/foo"+str(counter+1)+".png", x = (pdf.w - 175) / 2, w = 175, h = 175)

                    if (teamSideFilter != "Both sides"):
                        if teamSideFilter == "RED_TEAM":
                            pdf.set_text_color(213, 56, 56)
                        if teamSideFilter == "BLUE_TEAM":
                            pdf.set_text_color(0, 153, 224)
                    else:
                        if teamSide[j] == "RED_TEAM":
                            pdf.set_text_color(213, 56, 56)
                        if teamSide[j] == "BLUE_TEAM":
                            pdf.set_text_color(0, 153, 224)

                    pdf.multi_cell(0, 8, statsTitlesArray[counter].encode('latin-1', 'ignore').decode('latin-1'), align="C")
                    pdf.set_text_color(0, 0, 0)
                    
                    counter=counter+1

            dirPath="./data/reports/"+fileName+".pdf"
            # Creates the directory if it doesn't exist
            os.makedirs(os.path.dirname(dirPath), exist_ok = True)
            pdf.output(dirPath, 'F')

            files = glob.glob('./data/temp/*')
            for f in files:
                os.remove(f)
            if os.path.exists('./data/temp/') :
                os.rmdir('./data/temp')
        # else all games from this player history do not respect filters

def csvToPdfReport(region: str, rankLeague: str, summonerName: str, queueType: list, gameIds: list, role: str = None, teamSide: list=[], championsPlayed: list=[], teamSideFilter: str = None):
    """
    Creates a pdf file with data sent in region folder of the data folder.

    :param str region: The region of the CSVs 
    :param str rankLeague: The rank league (challenger, grandmaster or master)
    :param str summonerName: The summoner name
    :param list queueType: Array of type of queue (RANKED_FLEX_SR or RANKED_SOLO_5x5)
    :param list gameIds: Array of game id
    :param role: The role of the summoner
    :type role: str or None 
    :param list teamSide: Array of team side of the games retrieved (Red or blue)
    :param str championsPlayed: Array of champions filtered
    :param str teamSideFilter: the filter from the interface

    """
    pathToParticipant=""
    fileName=""

    match(teamSideFilter):
        case "Blue side":
            teamSideFilter="BLUE_TEAM"
        case "Red side":
            teamSideFilter="RED_TEAM"

    if (rankLeague == None and summonerName != None and queueType != None):

        stat = Statistics(region,summonerName,None)

        gamesPath = []

        # Loop through all the games retrieved
        for i in range(len(gameIds)):
            # Path of the csv files
            pathToParticipant = 'data/'+region+'/'+region+'_'+summonerName+'/'+queueType[i]+'/'+'participant'
            # If we provided a role, the path is different
            if role != None :
                pathToParticipant='data/'+region+'/'+region+'_'+role+"_"+summonerName+'/'+queueType[i]+'/'+'participant'

            filePath = pathToParticipant+'/'+gameIds[i]+'_participant.csv'
            # Store the game path in an array
            if not(filePath in gamesPath) :
                gamesPath.append(filePath)

        # check if all filters are correct
        numberOfIncorrectGames = 0
        for i in range(len(gameIds)):

            gameId=gameIds[i]

            # Get all participants from the good path
            pathToParticipant='data/'+region+'/'+region+'_'+summonerName+'/'+queueType[i]+'/'+'participant'
            # If we provided a role, the path is different
            if role != None :
                pathToParticipant='data/'+region+'/'+region+'_'+role+"_"+summonerName+'/'+queueType[i]+'/'+'participant'

            filePath=pathToParticipant+'/'+gameIds[i]+'_participant.csv'

            # Generate the creep score graph for a game and add the image to the pdf

            gameRespectFilters=False
            if len(championsPlayed) !=0 :
                # only one champ can be played for A SINGLE GAME, so no problems
                for j in range(len(championsPlayed)):
                    # the image will be created only if one of the champions in the filter is the one played during the game
                    gameRespectFilters=stat.doesGameRespectFilters(gameIds[i],role,filePath,championsPlayed[j],teamSide[i],teamSideFilter)
                    if gameRespectFilters :
                        # correct filters for championsPlayed[j]
                        break
            # no champions in filters
            else :
                gameRespectFilters=stat.doesGameRespectFilters(gameIds[i],role,filePath,None,teamSide[i],teamSideFilter)
            # to fix the pb of title, when a game used in csStatsOfOneGame is not returned due to filters
            # if we do not take account of this boolean below, 
            # then the data of the game that did not respect the filters will be used for the title
            if (not(gameRespectFilters)):
                numberOfIncorrectGames=numberOfIncorrectGames+1

        # Title data
        title = "Report of: " + summonerName
        if(role != None):
            title += " ("+role+")"
        if(gameIds != None and len(gameIds) != 0):
            title+="\n"
            title += str(len(gameIds)-numberOfIncorrectGames)
            if len(gameIds)-numberOfIncorrectGames!=1 :
                title+= " games "
            else :
                title+= " game "
            title+="("+ region +")"

        title=title.encode('latin-1', 'ignore').decode('latin-1')

        pdf=templateOfPdfReport(title)

        # Generate the global graph
        stat.csStatsOfGames(gameIds, role, gamesPath, championsPlayed, teamSide, teamSideFilter)

        if (os.path.exists("./data/temp/global1.png")) :
            pdf.add_page()
            pdf.image("./data/temp/global1.png", x = (pdf.w - 175) / 2, w = 175, h = 175)
            globalStatsName="Global creep score between " + summonerName + " and his opponents"
            pdf.multi_cell(0, 8, globalStatsName.encode('latin-1', 'ignore').decode('latin-1'), align="C")

        imageCounter=0
        # Loop through all games
        for i in range(len(gameIds)):

            gameId=gameIds[i]

            # Get all participants from the good path
            pathToParticipant='data/'+region+'/'+region+'_'+summonerName+'/'+queueType[i]+'/'+'participant'
            # If we provided a role, the path is different
            if role != None :
                pathToParticipant='data/'+region+'/'+region+'_'+role+"_"+summonerName+'/'+queueType[i]+'/'+'participant'

            filePath=pathToParticipant+'/'+gameIds[i]+'_participant.csv'

            # Generate the creep score graph for a game and add the image to the pdf

            gameRespectFilters=False
            if len(championsPlayed) != 0 :
                # only one champ can be played for A SINGLE GAME, so no problems
                for j in range(len(championsPlayed)):
                    # the image will be created only if one of the champions in the filter is the one played during the game
                    gameRespectFilters=stat.csStatsOfOneGame(gameIds[i],role,filePath,championsPlayed[j],teamSide[i],teamSideFilter)
                    if gameRespectFilters :
                        # correct filters for championsPlayed[j]
                        break
            # no champions in filters
            else :
                gameRespectFilters=stat.csStatsOfOneGame(gameIds[i],role,filePath,None,teamSide[i],teamSideFilter)
            # to fix the pb of title, when a game used in csStatsOfOneGame is not returned due to filters
            # if we do not take account of this boolean bellow, 
            # then the datas of the game that did not respect the filters will be used for the title
            if (gameRespectFilters):
                imageCounter = imageCounter + 1
                pdf.add_page()
                pdf.image("./data/temp/foo"+str(imageCounter)+".png", x = (pdf.w - 175) / 2, w = 175, h = 175)

                imageLegend = summonerName
                # If the role filter is set to fill, get the correct role for the current game to show it
                if (role == "FILL"):
                    ourSummonerRole = stat.getOurSummonerRole(filePath)
                    imageLegend += " (" + ourSummonerRole + "):\n"
                else:
                    imageLegend += " (" + role + "):\n"

                # Get summoners champions to put in the label
                ourSummonerChampName = stat.getOurSummonerChampionName(filePath)
                ourSummonerOpponentChampName = stat.getOurSummonerOpponentChampionName(filePath)

                imageLegend += "Creep score comparison between " + ourSummonerChampName + " and " + ourSummonerOpponentChampName
                if (queueType[i] == "RANKED_SOLO_5x5"):
                    imageLegend += "\n(Ranked Solo/Duo)"
                if (queueType[i] == "RANKED_FLEX_SR"):
                    imageLegend += "\n(Ranked Flex)"
                if teamSide[i]=="RED_TEAM":
                    pdf.set_text_color(213, 56, 56)
                else :
                    pdf.set_text_color(0, 153, 224)
                pdf.multi_cell(0, 8, imageLegend.encode('latin-1', 'ignore').decode('latin-1'), align="C")
                pdf.set_text_color(0, 0, 0)

        # If there is only one game in the array
        if len(gameIds) == 1 :
            gameId=gameIds[0]
            fileName=region+"_"+queueType[0]+"_"+summonerName+ "_" + role + "_" +gameId+"_"+"Report"
        else :
            if(checkAllSameInList(queueType)):
                fileName=region+"_"+queueType[0]+"_"+summonerName + "_" + role +"_"+"Report"
            else :   
                fileName=region+"_"+'ALL_QUEUES'+"_"+summonerName + "_" + role +"_"+"Report"
    # Otherwise, rankLeague if entered
    else:
        # If there is only one game in the array
        if len(gameIds) == 1 :
            gameId=gameIds[0]
            fileName=region+"_"+rankLeague+"_"+gameId+"_"+"Report"
        else :
            fileName=region+"_"+rankLeague+"_"+"_"+"Report"
        
    if numberOfIncorrectGames==len(gameIds):
        # All games are incorrect, no report produced
        return

    # Creates the directory if it doesn't exist and generate the PDF report
    os.makedirs(os.path.dirname("./data/reports/"+fileName+".pdf"), exist_ok = True)
    pdf.output("./data/reports/"+fileName+".pdf", 'F')

    files = glob.glob('./data/temp/*')
    # Remove the images in the temp folder
    for f in files:
        os.remove(f)
    # in case no graph has been produced
    if os.path.exists('./data/temp/') :
        os.rmdir('./data/temp')

def templateOfPdfReport(title:str="Report"):

    """
        The method that generate the template of the report

        param str title:Title of the report (by default Report)
    """

    class PDF(FPDF):
        def header(self):
            # Logo
            self.image("./media/logo/ucc_logo.png", 0.5, 5, 30)
            # Font
            self.set_font("helvetica", "B", 15)
            documentWidth = self.w
            documentHeight = self.h
            # Colors of text, rect fill and frame
            self.set_text_color(0, 90, 130)
            self.set_fill_color(0, 90, 130)
            self.set_draw_color(0, 90, 130)

            # Width of line
            self.set_line_width(0.8)
            # Create the line
            self.line(25, 15, documentWidth - 25, 15)
            # Create the rectangles
            self.rect(0, 0, 7, documentHeight, "DF")
            self.rect(documentWidth - 7, 0, 7, 30, "DF")

            # Create the circles
            for i in range(8):
                if (i % 2) == 0:
                    # Yellow
                    self.set_draw_color(200, 155, 60)
                else:
                    # Blue
                    self.set_draw_color(0, 90, 130)

                self.ellipse(documentWidth - 1.5 - (3 * i), documentHeight - 1.5, 1, 1, "DF")
                self.ellipse(documentWidth - (3 * i), documentHeight - 3.5, 1, 1, "DF")
                self.ellipse(documentWidth - 1.5 - (3 * i), documentHeight - 5.5, 1, 1, "DF")
                self.ellipse(documentWidth - (3 * i), documentHeight - 7.5, 1, 1, "DF")
                self.ellipse(documentWidth - 1.5 - (3 * i), documentHeight - 9.5, 1, 1, "DF")
                self.ellipse(documentWidth - (3 * i), documentHeight - 11.5, 1, 1, "DF")
                self.ellipse(documentWidth - 1.5 - (3 * i), documentHeight - 13.5, 1, 1, "DF")
                self.ellipse(documentWidth - (3 * i), documentHeight - 15.5, 1, 1, "DF")
                self.ellipse(documentWidth - 1.5 - (3 * i), documentHeight - 17.5, 1, 1, "DF")


            # Change the current position of x and y to align title to the center and put it below the line
            self.set_y(25)
            # Title
            self.multi_cell(0, 7, title.encode('latin-1', 'ignore').decode('latin-1'), align="C")
            # Line break
            self.ln(10)

        # Page footer
        def footer(self):
            # Set position of the footer
            self.set_y(-12)
            # set font
            self.set_font("helvetica", "BI", 8)
            # Page number
            self.cell(0, 10, f"Page {self.page_no()}", align="C")

    pdf = PDF("P", "mm", "A4")
    # metadata
    pdf.set_title(title.encode('latin-1', 'ignore').decode('latin-1'))
    pdf.set_author("Killian Maxel and Antonin Winterstein")

    # Set auto page break
    pdf.set_auto_page_break(auto = True, margin = 15)

    return pdf

def showCurrentTime():
    """
    Gives the current time.

    :return: a string containing the current time like follow: [HH:MM:SS]
    """
    now = datetime.now()
    currentTime = now.strftime("%H:%M:%S")
    return "[" + currentTime + "] "


def showExecutionTime(startTime: float):
    """
    Gives the total execution time of the program.

    :param float startTime: The starting time of the program
    :return: a string containing the execution time like follow: HH:MM:SS.MS
    """
    executionTime = str(timedelta(seconds = (time.time() - startTime)))
    return executionTime


def convertMillisecondsToMinutes(milliseconds: int):
    """
    Gives the conversion of sent milliseconds to corresponding minute.

    :param float milliseconds: The number of milliseconds we want to convert
    :return: an int containing the minute corresponding to the sent milliseconds
    """
    minutes = int((milliseconds / (1000 * 60)) % 60)

    return minutes


def convertMillisecondsToMinutesAndSeconds(milliseconds: int):
    """
    Gives the conversion of sent milliseconds to corresponding minutes and seconds.

    :param float milliseconds: The number of milliseconds we want to convert
    :return: a string containing the minutes and seconds corresponding to the sent milliseconds in the format mm:ss
    """
    minutes = int((milliseconds / (1000 * 60)) % 60)
    seconds = int((milliseconds / 1000) % 60)

    return str(minutes) + ":" + str(seconds)


def removeLastSpace(summonerName: str):
    """
    Removes the last whitespace if it exists and returns it.

    :param str summonerName: The summoner name to remove the space
    :return: a string containing the summoner name without the last space if it had a space
    """
    return "".join(summonerName.rstrip())
from utils.constants import lolWatcher
from utils.tools import jsonObjectToCSV
from utils.tools import showCurrentTime
from classes.Summoner import Summoner
from classes.Summoner import gameStringArray
# Import requestCounter to get the requestNumber
import utils.requestManager as requestManager

def getSummonersFromLeague(region: str, queueType: str, rankLeague: str):
  """
  Gets all players from challenger, grandmaster or master of a specific region and a specific queue (Solo queue or flex)

  :param str region: The region of the summoners
  :param str queueType: The queue type (RANKED_SOLO_5x5 or RANKED_FLEX_SR)
  :param str rankLeague: The rank league (challenger, grandmaster or master)
  :return: a list containing summoners ids and names of summoners retrieved from the corresponding region, queue and league
  """
  requestManager.incrementRequestNumber()
  requestManager.pauseCodeForTimeDelayIfMaxRequest()

  leagueData = None

  # Call to API and store data
  try:
    if(rankLeague == "challenger"):
      leagueData = lolWatcher.league.challenger_by_queue(region, queueType)

    if(rankLeague == "grandmaster"):
      leagueData = lolWatcher.league.grandmaster_by_queue(region, queueType)

    if(rankLeague == "master"):
      leagueData = lolWatcher.league.masters_by_queue(region, queueType)
  except:
    print(showCurrentTime() + "An exception occured while trying to get data of the " + queueType + " league: " + rankLeague + ". (" + region + ")")


  if (leagueData != None):
    entriesArrayLength = len(leagueData['entries'])

    entryStringArray = []
    # Loop through all entries of the league (i.e each player of the league)
    for i in range(entriesArrayLength):
      entry = leagueData['entries'][i]

      # Create a new object with the entry (summoner) informations
      entryObject = {
        "summonerId": entry['summonerId'],
        "summonerName": entry['summonerName']
      }

      # Adds the entry (summoner) to the array
      entryStringArray.append(entryObject)

    # Call the function to create the CSV file
    jsonObjectToCSV(entryStringArray, region, rankLeague = rankLeague, dataType = "summoners")

    return entryStringArray
  else:
    print(showCurrentTime() + "Error. Can't find data of the " + queueType + " league: " + rankLeague + ". (" + region + ")")


def getGamesOfPlayersFromLeague(region: str, queueType: str, rankLeague: str):
  """
  Gets games of all players from a specific queue (Solo queue or flex) for a specific rank league (challenger, grandmaster or master)

  :param str region: The region of the summoners
  :param str queueType: The queue type (RANKED_SOLO_5x5 or RANKED_FLEX_SR)
  :param str rankLeague: The rank league (challenger, grandmaster or master)
  :return: a list containing games ids of games retrieved from the corresponding region, queue and league
  """
  playersFromLeague = getSummonersFromLeague(region, queueType, rankLeague)

  # Get number of players retrieved
  playersFromLeagueArrayLength = len(playersFromLeague)

  # Loop through all the players retrieved
  for i in range(playersFromLeagueArrayLength):
    summonerId = playersFromLeague[i]['summonerId']
    summonerData = Summoner(region, summonerId)

    summonerData.getGameHistoryFromSummoner()

  jsonObjectToCSV(gameStringArray, region, rankLeague = rankLeague, dataType = "games")
  return gameStringArray

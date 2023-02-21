from riotwatcher import LolWatcher, ApiError
import json

# API_KEY = "RGAPI-b8936b47-85d6-46d4-99b0-28ef36099814"
# lolWatcher = LolWatcher(API_KEY)
timeDelay = 126 # Delay for 2 minutes 6 (126 seconds, 5% margin)

itemsList = []
# Opening JSON file
itemsFile = open("utils/items.json")
# returns JSON object as dict
itemsData = json.load(itemsFile)
# Iterating through the json list, and add its elements to array to store items and use them after
for i in itemsData :
    # print(i["name"],"\n")
    itemsList.append(i)

# Closing file
itemsFile.close()
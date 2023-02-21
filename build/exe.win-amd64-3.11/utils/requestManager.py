from utils.constants import timeDelay
from utils.tools import showCurrentTime
import time

requestNumber = 0

def incrementRequestNumber():
  """
  Increments the variable stocking the number of requests done.
  """
  global requestNumber
  requestNumber += 1

def pauseCodeForTimeDelayIfMaxRequest():
  """
  Checks if the maximum number of requests (100) is reached. If so, it pauses the code for 2 minutes in order for the key to refresh its requests.
  """
  global requestNumber
  if (requestNumber == 100):
    print(showCurrentTime() +  "Let's wait 2 minutes! (126 seconds exactly)")
    # Resets the counter
    requestNumber = 0
    # Stops the code for 126 seconds
    time.sleep(timeDelay)

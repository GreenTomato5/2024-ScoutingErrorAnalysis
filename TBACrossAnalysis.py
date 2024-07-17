import requests
import pandas as pd
import json
import os

import constants

# Constants
SCOUTING_DATA_PATH = constants.Global.SCOUTING_DATA_PATH
MAX_MATCH_NUMBER = constants.Global.MAX_MATCH_NUMBER
TBA_PATH = constants.TBAAnalysis.TBA_PATH

# Load Data
tba = requests.get("https://www.thebluealliance.com/api/v3/event/2024hop/matches", 
                    headers={"X-TBA-Auth-Key": 
                        constants.TBAAnalysis.TBA_API_kEY}).json()

raw_data = pd.read_csv(SCOUTING_DATA_PATH)
data = raw_data[raw_data["Match Number"] < MAX_MATCH_NUMBER]

# Saves the data to a file so i dont have to imagine what the dict looks like
if (not os.path.exists(TBA_PATH)):
    
    with open(TBA_PATH, "w") as scribbler:
        json.dump(tba, scribbler)

for match in tba:
    match_number = match["match_number"]    
    comp_level = match["comp_level"]
    
    # Makes sure match is within correct range and is a quals match (it got scouted)
    if (not comp_level == "qm" or not match_number < constants.Global.MAX_MATCH_NUMBER):
        continue


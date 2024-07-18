import requests
import pandas as pd
import json
import os

import constants

# Constants
SCOUTING_DATA_PATH = constants.Global.SCOUTING_DATA_PATH
MAX_MATCH_NUMBER = constants.Global.MAX_MATCH_NUMBER
TBA_PATH = constants.TBAAnalysis.TBA_PATH
SHOW_MISSED_MATCHES = constants.TBAAnalysis.SHOW_MISSED_MATCHES

class TBACrossAnalysis:
    
    def __init__(self):
        # Load Data
        self.tba = requests.get("https://www.thebluealliance.com/api/v3/event/2024hop/matches", 
                            headers={"X-TBA-Auth-Key": 
                                constants.TBAAnalysis.TBA_API_kEY}).json()

        raw_data = pd.read_csv(SCOUTING_DATA_PATH)
        self.data = raw_data[raw_data["Match Number"] < MAX_MATCH_NUMBER]

        self.entries_checked = 0;

        self.cross_line_errors = []
        self.climb_errors = []

        # Saves the data to a file so i dont have to imagine what the dict looks like
        if (not os.path.exists(TBA_PATH)):
            with open(TBA_PATH, "w") as scribbler:
                json.dump(self.tba, scribbler)
            
    def error(self, scout, simple_error_type, assignment):
        return [scout, simple_error_type, assignment]

    def match_error(self, alliance, discrepancy, scoring_location, assignment):
        return [alliance, discrepancy, scoring_location, assignment]

    def crossCheckData(self):
        for match in self.tba:
            match_number = match['match_number']    
            comp_level = match['comp_level']
            
            # Makes sure match is within correct range and is a quals match (it got scouted)
            if (not comp_level == "qm" or not match_number < constants.Global.MAX_MATCH_NUMBER):
                continue
            
            for Alliance in ["Red", "Blue"]:
                for team_id in [1, 2, 3]:
                    assignment = f"{Alliance} {team_id}"
                    filtered_data = self.data[(self.data['Match Number'] == match_number) & (self.data["Assignment"] == assignment)]
            
                    if (len(filtered_data.index) == 1):
                        tba_cross_line = str(filtered_data['Crossed Line?'].iloc[0]).lower()
                        scouting_cross_line = "true" if str(match["score_breakdown"][Alliance.lower()][f"autoLineRobot{team_id}"]).lower() == "yes" else "false"
                        
                        if (tba_cross_line != scouting_cross_line):
                            self.cross_line_errors.append(self.error(filtered_data["Name"].iloc[0], "Crossed Line", assignment))
                        
                        tba_robot_climbed = match["score_breakdown"][Alliance.lower()][f"endGameRobot{team_id}"] != "None"
                        scouting_robot_climbed = filtered_data["Climb Type"].iloc[0] != None
                        
                        if (tba_robot_climbed != scouting_robot_climbed):
                            self.climb_errors.append(self.error(filtered_data["Name"].iloc[0], "Climb", assignment))                 
                    
                        self.entries_checked += 1
                    elif (SHOW_MISSED_MATCHES):
                        print(f"Match {match_number} {assignment} scouted {len(filtered_data.index)} times :(")  
                        
    def outputAnalysisResults(self):   
        print(f"Around {round(len(self.cross_line_errors)/self.entries_checked * 100, 2)}% of entries had a crossed line error")
        print(f"Around {round(len(self.climb_errors)/self.entries_checked * 100, 2)}% of entries had a climb error")
    
    def getErrors(self):
        return self.cross_line_errors + self.climb_errors
    
    def getEntriesChecked(self):
        return self.entries_checked
import csv
import os
import pandas as pd
import constants

# Constants
MISSED_SHIFT_PATH = constants.MissedShiftAnalysis.MISSED_SHIFT_PATH
MAX_MATCH_NUMBER = constants.Global.MAX_MATCH_NUMBER
SCOUTING_DATA_PATH = constants.Global.SCOUTING_DATA_PATH
ASSIGNMENTS = constants.Global.ASSIGNMENTS
SHIFTS = constants.Global.SHIFTS
SHIFT_A = constants.Global.SHIFT_A
SHIFT_B = constants.Global.SHIFT_B
SHIFT_C = constants.Global.SHIFT_C

class MissedShiftAnalysis:
    def __init__(self):
        if os.path.exists(MISSED_SHIFT_PATH) and os.path.getsize(MISSED_SHIFT_PATH) > 0:
            os.remove(MISSED_SHIFT_PATH)
            with open(MISSED_SHIFT_PATH, 'w', encoding="utf-8"):
                pass
            print("Replaced Existing Storage File")
        
        # Load and filter data
        raw_data = pd.read_csv(SCOUTING_DATA_PATH)
        self.data = raw_data[raw_data["Match Number"] < MAX_MATCH_NUMBER]

        # Initialize shift lists
        self.shift_A = SHIFT_A
        self.shift_B = SHIFT_B
        self.shift_C = SHIFT_C

    def current_shift(self, match_number):
        return SHIFTS[(match_number - 1) // 15 % 3]

    def error(self, scouter, match, scouter_assignment):
        return [scouter, match, scouter_assignment]

    def checkMissedShifts(self):
        shift_miss_errors = []
        for match in range(1, MAX_MATCH_NUMBER):
            filtered_match_data = self.data[self.data['Match Number'] == match]
            if len(filtered_match_data) < 6:
                remaining = 6
                for assignment in ASSIGNMENTS:
                    if not filtered_match_data["Assignment"].isin([assignment]).any():
                        remaining -= 1
                        current_shift_name = self.current_shift(match)
                        current_shift_list = self.shift_A if current_shift_name == "A" else (self.shift_B if current_shift_name == "B" else self.shift_C)
                        scout = current_shift_list[ASSIGNMENTS.index(assignment)]
                        scout[1] += 1
                        shift_miss_errors.append(self.error(scout[0], match, assignment))
                    if remaining == len(filtered_match_data):
                        break
        return shift_miss_errors

    def outputAnalysisResults(self):
        combined_shifts = self.shift_A + self.shift_B + self.shift_C

        if constants.MissedShiftAnalysis.SAVE_MISSED_SHIFTS:
            with open(MISSED_SHIFT_PATH, 'w', encoding="utf-8", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Scout", "Matches Missed"])
                writer.writerows(combined_shifts)
        
        for scout in combined_shifts:
            print(f"{scout[0]} missed {scout[1]} matches")
    
    def getMissedShifts(self):
        return self.shift_A + self.shift_B + self.shift_C
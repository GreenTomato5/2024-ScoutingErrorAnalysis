import csv
import os
import pandas as pd
import constants
import difflib


# Constants
MISSED_SHIFT_PATH = constants.MissedShiftAnalysis.MISSED_SHIFT_PATH
MAX_MATCH_NUMBER = constants.Global.MAX_MATCH_NUMBER
SCOUTING_DATA_PATH = constants.Global.SCOUTING_DATA_PATH
ASSIGNMENTS = constants.Global.ASSIGNMENTS
SHIFTS = constants.Global.SHIFTS
SHIFT_A = constants.Global.SHIFT_A
SHIFT_B = constants.Global.SHIFT_B
SHIFT_C = constants.Global.SHIFT_C
DOUBLE_SCOUTING = constants.Global.DOUBLE_SCOUTING

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
        return SHIFTS[(match_number - 1) // 15 % constants.CURRENT_EVENT.number_of_shifts]

    def error(self, scouter, match, scouter_assignment):
        return [scouter, match, scouter_assignment] 

    def closest_string_value(self, reference, options):
        similarities = [difflib.SequenceMatcher(None, reference, option).ratio() for option in options]
        if similarities[0] > similarities[1]:
            return 1
        else:
            return 3

    def checkMissedShifts(self):
        shift_miss_errors = []
        for match in range(1, MAX_MATCH_NUMBER):
            filtered_match_data = self.data[self.data['Match Number'] == match]
            if (not DOUBLE_SCOUTING):
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
            else:
                if len(filtered_match_data) < 12:
                    remaining = 12
                    for assignment in ASSIGNMENTS:
                        times_scouted = filtered_match_data["Assignment"].isin([assignment]).sum()
                        if (times_scouted < 2):
                            current_shift_name = self.current_shift(match)
                            current_shift_list = self.shift_A if current_shift_name == "A" else self.shift_B
                            scout = current_shift_list[ASSIGNMENTS.index(assignment)]
                            if (times_scouted == 0):
                                remaining -= 2
                                scout[1] += 1
                                scout[3] += 1
                            elif times_scouted == 1:
                                remaining -= 1
                                further_filtered = filtered_match_data[filtered_match_data['Assignment' == assignment]]
                                scout[self.closest_string_value(further_filtered['Name'].iloc[0], [scout[0], scout[2]])] += 1
                    if remaining == len(filtered_match_data):
                            break
        return shift_miss_errors

    def outputAnalysisResults(self):
        combined_shifts = self.shift_A + self.shift_B + self.shift_C

        if constants.MissedShiftAnalysis.SAVE_MISSED_SHIFTS:
            with open(MISSED_SHIFT_PATH, 'w', encoding="utf-8", newline='') as f:
                writer = csv.writer(f)
                if (DOUBLE_SCOUTING):
                    writer.writerow(["Scout1", "Matches Missed", "Scout2", "Matches Missed"])
                else:
                    writer.writerow(["Scout", "Matches Missed"])
                writer.writerows(combined_shifts)
        
        for scout in combined_shifts:
            print(f"{scout[0]} missed {scout[1]} matches")
    
    def getMissedShifts(self):
        return self.shift_A + self.shift_B + self.shift_C
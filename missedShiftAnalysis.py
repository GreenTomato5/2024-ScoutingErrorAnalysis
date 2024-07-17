import csv
import os
import pandas as pd
import constants

# Constants
MISSED_SHIFT_PATH = constants.MissedShiftAnalysis.MISSED_SHIFT_PATH
MAX_MATCH_NUMBER = constants.MissedShiftAnalysis.MAX_MATCH_NUMBER
SCOUTING_DATA_PATH = constants.Global.SCOUTING_DATA_PATH
ASSIGNMENTS = constants.Global.ASSIGNMENTS
SHIFTS = constants.Global.SHIFTS
shift_A = constants.Global.SHIFT_A
shift_B = constants.Global.SHIFT_B
shift_C = constants.Global.SHIFT_C

# Setup file to write to
if os.path.exists(MISSED_SHIFT_PATH) and os.path.getsize(MISSED_SHIFT_PATH) > 0:
    os.remove(MISSED_SHIFT_PATH)
    with open(MISSED_SHIFT_PATH, 'w', encoding="utf-8"):
        pass
    print("Replaced Existing Storage File")

# Load and filter data
raw_data = pd.read_csv(SCOUTING_DATA_PATH)
data = raw_data[raw_data["Match Number"] < MAX_MATCH_NUMBER]

def current_shift(match_number):
    return SHIFTS[(match_number - 1) // 15 % 3]

def error(scouter, match, scouter_assignment):
    return [scouter, match, scouter_assignment]

# Check missed shifts
shift_miss_errors = []
for match in range(1, MAX_MATCH_NUMBER):
    filtered_match_data = data[data['Match Number'] == match]
    if len(filtered_match_data) < 6:
        remaining = 6
        for assignment in ASSIGNMENTS:
            if not filtered_match_data["Assignment"].isin([assignment]).any():
                remaining -= 1
                current_shift_name = current_shift(match)
                current_shift_list = shift_A if current_shift_name == "A" else (shift_B if current_shift_name == "B" else shift_C)
                scout = current_shift_list[ASSIGNMENTS.index(assignment)]
                scout[1] += 1
                shift_miss_errors.append(error(scout[0], match, assignment))
            if remaining == len(filtered_match_data):
                break

# Combine shifts and write to CSV
combined_shifts = shift_A + shift_B + shift_C

with open(MISSED_SHIFT_PATH, 'w', encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Scout", "Matches Missed"])
    writer.writerows(combined_shifts)

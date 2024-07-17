import csv
import os
import pandas as pd

# Constants

MISSED_SHIFT_FILE = "MissedShifts.csv"
SCOUTING_DATA_FILE = "ScoutingData.csv"

MAX_MATCH_NUMBER = 109

ASSIGNMENTS = ["Red 1", "Red 2", "Red 3", "Blue 1", "Blue 2", "Blue 3"]
SHIFTS = ["A", "B", "C"]

# Setup File to Write To
if (os.path.exists(MISSED_SHIFT_FILE) and not os.stat(MISSED_SHIFT_FILE).st_size == 0):
    os.remove(MISSED_SHIFT_FILE) 
    open(MISSED_SHIFT_FILE, 'w', encoding="utf-8")
    print("Replaced Existing Storage File")

# Setup Important Variables
raw_data = pd.read_csv(SCOUTING_DATA_FILE)
data = raw_data[raw_data["Match Number"] < MAX_MATCH_NUMBER]

shift_A = [["Logan", 0], ["Fanta", 0], ["Davin", 0], ["Lucas", 0], ["Coby", 0], ["Leif", 0]]
shift_B = [["Luke", 0], ["Jazlyn", 0], ["Taj", 0], ["Jonathan", 0], ["Dillon", 0], ["Aiden", 0]]
shift_C = [["Karos", 0], ["Danyar", 0], ["Noah", 0], ["Freya", 0], ["Jalen", 0], ["Garys", 0]]

shift_miss_errors = []

# Functions for determining shifts and error input
def current_shift(match_number):
    i = match_number
    x = 0
    while (i > 15):
        i -= 15
        x +=1
        if (x == 3):
            x = 0
    return SHIFTS[x] 

def error(scouter, match, scouter_assignment):
    return [scouter, match, scouter_assignment]

# Check Missed Shifts     
for match in range(1, MAX_MATCH_NUMBER):
    filteredMatchData = data[data['Match Number'] == match]
    amountOfEntries = len(filteredMatchData)
    if (amountOfEntries < 6):
        remaining = 6
        for assignment in ASSIGNMENTS:
            if (not filteredMatchData["Assignment"].isin([assignment]).any()):
                remaining -= 1
                currentShift = current_shift(match)
                scout = (shift_A if currentShift == "A" else (shift_B if currentShift == "B" else shift_C))[
                        ASSIGNMENTS.index(assignment)
                        ]
                scout[1] += 1
                shift_miss_errors.append(error(
                    scout[0],
                    match,
                    assignment
                ))
            if (remaining == amountOfEntries):
                break
# Print out un-scouted matches

# for error in shift_miss_errors:
#     print(f'Match {error[1]} {error[2]} ({error[0]}) not scouted')
    
combined_shifts = shift_A + shift_B + shift_C

with open(MISSED_SHIFT_FILE, 'w', encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Scout", "Matches Missed"])
        writer.writerows(combined_shifts)




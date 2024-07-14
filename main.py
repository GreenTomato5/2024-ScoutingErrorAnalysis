import csv
import os
import pandas as pd

# Setup File to Write To
if (os.path.exists("MissedShifts.csv") and not os.stat("MissedShifts.csv").st_size == 0):
    os.remove("MissedShifts.csv") 
    open("MissedShifts.csv", 'w', encoding="utf-8")
    print("Replaced Existing Storage File")

# Setup Important Variables
raw_data = pd.read_csv("ScoutingData.csv")
max_match_number = 109
data = raw_data[raw_data["Match Number"] < max_match_number]

assignments = ["Red 1", "Red 2", "Red 3", "Blue 1", "Blue 2", "Blue 3"]

shift_A = [["Logan", 0], ["Fanta", 0], ["Davin", 0], ["Lucas", 0], ["Coby", 0], ["Leif", 0]]
shift_B = [["Luke", 0], ["Jazlyn", 0], ["Taj", 0], ["Jonathan", 0], ["Dillon", 0], ["Aiden", 0]]
shift_C = [["Karos", 0], ["Danyar", 0], ["Noah", 0], ["Freya", 0], ["Jalen", 0], ["Garys", 0]]

shift_miss_errors = []

# Functions for determining shifts and error input
def CurrentShift(match_number):
    i = match_number
    shifts = ["A", "B", "C"]
    x = 0
    while (i > 15):
        i -= 15
        x +=1
        if (x == 3):
            x = 0
    return shifts[x] 

def error(scouter, match, scouter_assignment):
    return [scouter, match, scouter_assignment]

# Check Missed Shifts     
for match in range(1, max_match_number):
    filteredMatchData = data[data['Match Number'] == match]
    amountOfEntries = len(filteredMatchData)
    if (amountOfEntries < 6):
        remaining = 6
        for assignment in assignments:
            if (not filteredMatchData["Assignment"].isin([assignment]).any()):
                remaining -= 1
                currentShift = CurrentShift(match)
                scout = (shift_A if currentShift == "A" else (shift_B if currentShift == "B" else shift_C))[
                        assignments.index(assignment)
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

with open("MissedShifts.csv", 'w', encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Scout", "Matches Missed"])
        writer.writerows(combined_shifts)




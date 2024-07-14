import os
import pandas as pd

# Setup File to Write To
if (os.path.exists("Storage.csv") and not os.stat("Storage.csv").st_size == 0):
    os.remove("Storage.csv") 
    open("Storage.csv", 'w', encoding="utf-8")
    print("Replaced Existing Storage File")

# Setup Important Variables
rawData = pd.read_csv("ScoutingData.csv")
maxMatchNumber = 109
data = rawData[rawData["Match Number"] < maxMatchNumber]

assignments = ["Red 1", "Red 2", "Red 3", "Blue 1", "Blue 2", "Blue 3"]

shiftA = ["Logan", "Fanta", "Davin", "Lucas", "Coby", "Leif"]
shiftB = ["Luke", "Jazlyn", "Taj", "Jonathan", "Dillon", "Aiden"]
shiftC = [ "Karos", "Danyar", "Noah", "Freya", "Jalen", "Garys"]

errors = []

def CurrentShift(matchNumber):
    i = matchNumber
    shifts = ["A", "B", "C"]
    x = 0
    while (i > 15):
        i -= 15
        x +=1
        if (x == 3):
            x = 0
    return shifts[x] 

def error(scouter, matchNumber, assigment):
    return [scouter, matchNumber, assignment]

# Check Missed Shifts
      
for entry in range(1, maxMatchNumber):
    filteredMatchData = data[data['Match Number'] == entry]
    amountOfEntries = len(filteredMatchData)
    if (amountOfEntries < 6):
        remaining = 6
        for assignment in assignments:
            if (not filteredMatchData["Assignment"].isin([assignment]).any()):
                remaining -= 1
                currentShift = CurrentShift(entry)
                errors.append(error(
                    (shiftA if currentShift == "A" else (shiftB if currentShift == "B" else shiftC))[
                        assignments.index(assignment)
                        ],
                    entry,
                    assignment
                ))
            if (remaining ==amountOfEntries):
                break
print(errors)

    





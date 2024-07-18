import missed_shift_analysis
import TBA_cross_analysis
import constants

# Run analyses, save data, create important variables, define important functions
COMBINED_SHIFTS = constants.Global.COMBINED_SHIFTS

missed_shifts_analysis = missed_shift_analysis.MissedShiftAnalysis()
missed_shifts_analysis.checkMissedShifts()

tba_analysis = TBA_cross_analysis.TBACrossAnalysis()
tba_analysis.crossCheckData()

missed_shifts = missed_shifts_analysis.getMissedShifts()
cross_analysis_errors = tba_analysis.getErrors()

cross_entries_checked = tba_analysis.getEntriesChecked()

scouter_grades = []

def getLetterGrade(grade):
    possible_grades = [["A", 90], ["B", 80], ["C", 70], ["D", 60], ["F", 50], [":(", 0]]
    sign_cutoffs = [["+", 7], ["", 4], ["-", 0]]
    
    for grade_possibility in possible_grades:
        if (grade > grade_possibility[1]):
            sign_score = grade - grade_possibility[1]
            for sign_possibiliy in sign_cutoffs:
                if (sign_score > sign_possibiliy[1]):
                    sign = sign_possibiliy[0]
                    break
            return f"{grade_possibility[0]}{sign}"
        
# Calculate Scouter Grades
def calculateScouterGrades():
    for scout in COMBINED_SHIFTS:
        name = scout[0]
        filtered_cross_data = list(filter(lambda subarray: subarray[0] == name, cross_analysis_errors))
        filtered_missed_data = list(filter(lambda subarray: subarray[0] == name, missed_shifts))
        
        # Divide "filtered_cross_data" by 2 to go off errors per-match
        accuracy = round(((cross_entries_checked - len(filtered_cross_data))/cross_entries_checked) * 100, 2)
        letter_grade = getLetterGrade(accuracy)
        matches_missed = filtered_missed_data[0][1]
        matches_scouted = filtered_missed_data[0][2]
        
        scouter_grades.append([accuracy, letter_grade, matches_missed, name, matches_scouted])
    scouter_grades.sort(key=lambda subarray: subarray[0], reverse = True)

# Output Data
calculateScouterGrades()
for grade in scouter_grades:
    print(f"{grade[3]} got a {grade[1]} with {grade[0]}% accuracy and missed {grade[2]} matches out of {grade[4]} matches")
        


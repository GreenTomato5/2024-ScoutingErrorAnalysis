import pandas as pd

class MissedShiftAnalysis:
    MISSED_SHIFT_PATH = "Data/MissedShifts.csv"
    SAVE_MISSED_SHIFTS = False;

class Global:
    SCOUTING_DATA_PATH = "Data/ScoutingData.csv"
    ASSIGNMENTS = ["Red 1", "Red 2", "Red 3", "Blue 1", "Blue 2", "Blue 3"]
    SHIFTS = ["A", "B", "C"]
    SHIFT_A = [["Logan", 0], ["Fanta", 0], ["Davin", 0], ["Lucas", 0], ["Coby", 0], ["Leif", 0]]
    SHIFT_B = [["Luke", 0], ["Jazlyn", 0], ["Taj", 0], ["Jonathan", 0], ["Dillon", 0], ["Aiden", 0]]
    SHIFT_C = [["Karos", 0], ["Danyar", 0], ["Noah", 0], ["Freya", 0], ["Jalen", 0], ["Garys", 0]]
    COMBINED_SHIFTS = SHIFT_A + SHIFT_B + SHIFT_C
    MAX_MATCH_NUMBER = 109

class TBAAnalysis:
    TBA_API_kEY = ""
    TBA_PATH = "Data/TBA.json"
    SHOW_MISSED_MATCHES = False;
    


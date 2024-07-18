import pandas as pd

class MissedShiftAnalysis:
    MISSED_SHIFT_PATH = "Data/MissedShifts.csv"
    SAVE_MISSED_SHIFTS = False;

class Global:
    SCOUTING_DATA_PATH = "Data/ScoutingData.csv"
    ASSIGNMENTS = ["Red 1", "Red 2", "Red 3", "Blue 1", "Blue 2", "Blue 3"]
    SHIFTS = ["A", "B", "C"]
    MAX_MATCH_NUMBER = 109
    
    # Calculate matches per shift
    MATCHES_PER_SHIFT = MAX_MATCH_NUMBER // 3
    MATCH_REMAINDER = MAX_MATCH_NUMBER % 15
    
    LAST_SHIFT = MAX_MATCH_NUMBER // 15 % 3
    
    MATCHES_A = MATCHES_PER_SHIFT + (MATCH_REMAINDER if LAST_SHIFT == 1 else 0)
    MATCHES_B = MATCHES_PER_SHIFT + (MATCH_REMAINDER if LAST_SHIFT == 2 else 0)
    MATCHES_C = MATCHES_PER_SHIFT + (MATCH_REMAINDER if LAST_SHIFT == 0 else 0)
    
    # this is an abomination
    SHIFT_A = [["Logan", 0, MATCHES_A], ["Fanta", 0, MATCHES_A], ["Davin", 0, MATCHES_A], ["Lucas", 0, MATCHES_A], ["Coby", 0, MATCHES_A], ["Leif", 0, MATCHES_A]]
    SHIFT_B = [["Luke", 0, MATCHES_B], ["Jazlyn", 0, MATCHES_B], ["Taj", 0, MATCHES_B], ["Jonathan", 0, MATCHES_B], ["Dillon", 0, MATCHES_B], ["Aiden", 0, MATCHES_B]]
    SHIFT_C = [["Karos", 0, MATCHES_C], ["Danyar", 0, MATCHES_C], ["Noah", 0, MATCHES_C], ["Freya", 0, MATCHES_C], ["Jalen", 0, MATCHES_C], ["Garys", 0, MATCHES_C]]

    COMBINED_SHIFTS = SHIFT_A + SHIFT_B + SHIFT_C

class TBAAnalysis:
    TBA_API_kEY = ""
    TBA_PATH = "Data/TBA.json"
    SHOW_MISSED_MATCHES = False;
    


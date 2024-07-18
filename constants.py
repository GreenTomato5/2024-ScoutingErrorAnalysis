import pandas as pd
from enum import Enum

class MissedShiftAnalysis:
    MISSED_SHIFT_PATH = "Data/MissedShifts.csv"
    SAVE_MISSED_SHIFTS = False;

class Global:
    SCOUTING_DATA_PATH = "Data/Arkansas.csv"
    ASSIGNMENTS = ["Red 1", "Red 2", "Red 3", "Blue 1", "Blue 2", "Blue 3"]
    SHIFTS = ["A", "B", "C"]
    MAX_MATCH_NUMBER = 109
    
    class Events(Enum):
        WORLDS = 3, False, [["Logan", 0], ["Fanta", 0], ["Davin", 0], ["Lucas", 0], ["Coby", 0], ["Leif", 0]], [["Luke", 0], ["Jazlyn", 0], ["Taj", 0], ["Jonathan", 0], ["Dillon", 0], ["Aiden", 0]], [["Karos", 0], ["Danyar", 0], ["Noah", 0], ["Freya", 0], ["Jalen", 0], ["Garys", 0]]
        
        BUCKEYE = 2, True, [["John", 0, "Davin", 0], ["Owen", 0, "Aros", 0], ["Danyar", 0, "Karos", 0], ["Aiden", 0, "Luke", 0], ["Coby", 0, "Logan", 0], ["Shubh", 0, "Alex", 0]], [["Freya", 0, "Davin", 0], ["Abhi", 0, "Nick", 0], ["Noah", 0, "Jazlyn", 0], ["Aiden", 0, "Fanta", 0], ["Johnathan", 0, "Ridge", 0], ["Lucia", 0, "Sofiya", 0]], []
        
        ARKANSAS = 2, True, [["Freya", 0, "Dillon", 0], ["Zofia", 0, "Jazlyn", 0], ["Taj", 0, "Luke", 0], ["Aiden", 0, "Garys", 0], ["Coby", 0, "Jalen", 0], ["Leif", 0, "Alex", 0]], [["Aros", 0, "Karos", 0], ["Danyar", 0, "Maggie", 0], ["Noah", 0, "Logan", 0], ["Damari", 0, "Fanta", 0], ["Johnathan", 0, "Ridge", 0], ["Lucia", 0, "Sofiya", 0]], []
        
        def __init__(self, number_of_shifts, double_scouted, shift_A, shift_B, shift_C):
            self.number_of_shifts = number_of_shifts
            self.double_scouted = double_scouted
            self.shift_A = shift_A
            self.shift_B = shift_B
            self.shift_C = shift_C
        
    CURRENT_EVENT = Events.ARKANSAS
    DOUBLE_SCOUTING = CURRENT_EVENT.double_scouted

    # Calculate matches per shift
    MATCHES_PER_SHIFT = MAX_MATCH_NUMBER // CURRENT_EVENT.number_of_shifts
    MATCH_REMAINDER = MAX_MATCH_NUMBER % 15
    LAST_SHIFT = MAX_MATCH_NUMBER // 15 % CURRENT_EVENT.number_of_shifts

    MATCHES_A = MATCHES_PER_SHIFT + (MATCH_REMAINDER if LAST_SHIFT == 0 else 0)
    MATCHES_B = MATCHES_PER_SHIFT + (MATCH_REMAINDER if LAST_SHIFT == 1 else 0)
    MATCHES_C = MATCHES_PER_SHIFT + (MATCH_REMAINDER if LAST_SHIFT == 2 else 0)

    SHIFT_A = CURRENT_EVENT.shift_A
    SHIFT_B = CURRENT_EVENT.shift_B
    SHIFT_C = CURRENT_EVENT.shift_C

    for scouter in SHIFT_A:
        scouter.append(MATCHES_A)
    for scouter in SHIFT_B:
        scouter.append(MATCHES_B)
    if (not CURRENT_EVENT.double_scouted):
        for scouter in SHIFT_C:
            scouter.append(MATCHES_C)
            
    COMBINED_SHIFTS = SHIFT_A + SHIFT_B + SHIFT_C
class TBAAnalysis:
    TBA_API_kEY = ""
    TBA_PATH = "Data/TBA.json"
    SHOW_MISSED_MATCHES = False;
    


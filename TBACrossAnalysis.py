import requests

# Constants
SCOUTING_DATA_PATH = "CSVs/ScoutingData.csv"
MAX_MATCH_NUMBER = 109

# Load TBA data (zzz my API key is most def NOT going in here)
tba = requests.get("https://www.thebluealliance.com/api/v3/event/2024hop/matches", 
                   headers={"X-TBA-Auth-Key": 
                       ""}).json()

raw_data = pd.read_csv(SCOUTING_DATA_PATH)
data = raw_data[raw_data["Match Number"] < MAX_MATCH_NUMBER]
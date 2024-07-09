import requests
import json

# Census Meta data with link that defines variables
url = 'https://api.census.gov/data/2022/acs/acs5/subject/variables.json'
response = requests.get(url)
data = response.json()

# Filters over a 150000 entries to just the ones with the S0101_C01 code
s0101_entries = {key: value for key, value in data['variables'].items() if 'S0101_C01' in key}
print(json.dumps(s0101_entries, indent=2))
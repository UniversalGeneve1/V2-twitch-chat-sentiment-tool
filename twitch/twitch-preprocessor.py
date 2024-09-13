import csv, json, sys
import pandas as pd

sys.path.append('../common')
from common_utils import write_to_store

streamer = (sys.argv[1]).lower() 

col_names = [
	'timestamp',
	'action_type',
	'message_type',
	'message',
	'user_type',
	'is_first_message',
	'is_returning_chatter',
	'is_vip',
	'message',
	'is_moderator', #author
	'is_subscriber',
	'is_turbo',
	'badge1_name', #author - badges
	'badge1_title',
	'badge2_name',
	'badge2_title',
	'badge3_name',
	'badge3_title',
	'badge4_name',
	'badge4_title'
]


def data_impute(obj, key):
	if key in obj:
		return obj[key]
	return None

def process_twitch_user_badge_data(badges):

	badge_data = []
	if 'badges' in badges:
		padding = 4 - len(badges['badges'])
		for b in badges['badges']:
			[badge_data.append(data_impute(b, k)) for k in ['name', 'title']]
		badge_data = badge_data + (padding * [None, None]) #pad with None if user has less than 4 badges 
	else:
		badge_data = (8*[None])
	return badge_data

#TODO: figure out how to load files into this process via the tracking files

file_to_process = "RAW_frostyphrosty_2024-08-03_023247.jsonl"
file_id_name = file_to_process.split(".")[0]
landing_file = f"data/{streamer}/preprocessed/{file_id_name}.csv"

data = []
	
with open(file_to_process, 'r') as file:
	for line in file:
		row = []
		json_object = json.loads(line.strip())
		[row.append(data_impute(json_object, x)) for x in col_names[:9]] #first 10 cols are top level
		[row.append(data_impute(json_object['author'], x)) for x in col_names[9:12]] # cols 11-13 are in author object
		row = row + process_twitch_user_badge_data(json_object['author'])
		data.append(row)
		
df = pd.DataFrame(data, columns=col_names)
df['timestamp'] = pd.to_datetime(df['timestamp']/1000, unit = 'ms')


df.to_csv(landing_file)
write_to_store("twitch", streamer, landing_file, "preprocessed")


			
			
		
	




		












	














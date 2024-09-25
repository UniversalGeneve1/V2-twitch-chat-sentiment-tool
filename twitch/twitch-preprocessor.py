import os
from numpy import loadtxt
import csv, json, sys
import pandas as pd

sys.path.append('../common')
from common_utils import write_to_store

streamer = (sys.argv[1]).lower() 
base_dir = f"data/{streamer}/preprocessed"

bot_names = [
	'nightbot',
	'fossabot',
	'streamelements',
	'nightbot',
	'moobot',
	'pokemoncommunitygame',
	'sery_bot',
	'kofistreambot',
	'songlistbot',
	'irltoolkit'	
]

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
	'badge1_name', #author - badges. users have max 4 badges
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


###

preproc_files_tracking = f"{base_dir}/tracking.txt"

ran_files = []

with open(preproc_files_tracking, 'r') as tf:
	for ln in tf:
		ran_files.append(ln)

files_to_run = [f for f in os.listdir(f"data/{streamer}/raw") if f not in ran_files and f!= 'tracking.txt']

for f2r in files_to_run: 
	file_loc = f"data/{streamer}/raw/{f2r}"
	print(file_loc)
	file_id_name = "PREPROC_" + f2r.split(".")[0][4:]
	landing_file = f"{base_dir}/{file_id_name}.csv"

	data = []	
	with open(file_loc, 'r') as file:
		for line in file:
			row = []
			json_object = json.loads(line.strip())
			if (json_object['author']['display_name']).lower() in bot_names:
				continue
			[row.append(data_impute(json_object, x)) for x in col_names[:9]] #first 10 cols are top level
			[row.append(data_impute(json_object['author'], x)) for x in col_names[9:12]] # cols 11-13 are in author object
			row = row + process_twitch_user_badge_data(json_object['author'])
			data.append(row)
			
	df = pd.DataFrame(data, columns=col_names)
	df['timestamp'] = pd.to_datetime(df['timestamp']/1000, unit = 'ms')
	#print(df)

	df.to_csv(landing_file)
	write_to_store("twitch", streamer, landing_file, "preprocessed")


			
			
		
	




		












	














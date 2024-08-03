from chat_downloader import ChatDownloader
from datetime import datetime
from time import sleep
from twitch_live_sensor import twitch_sensor_check
import json, os, random, sys

streamer = sys.argv[1] 
url = f"https://www.twitch.tv/{streamer.lower()}"

### main:
# start live listener
# once live, generate files then start scrape, timeout will handle termination of scrape
# write to nas

while twitch_sensor_check(url) == False:
	print(f"{streamer} not live")
	sleep((29 + random.uniform(0, 5)))
	continue
	
print(f"{streamer} has gone live! Starting scrape")

todays_date = datetime.now().strftime('%Y-%m-%d')
time_of_trigger = datetime.now().strftime('%H%M%S')
streamer_dir_root = f"data/{streamer}"

#make dirs and file
os.makedirs(f"{streamer_dir_root}/preprocessed", exist_ok=True)
os.makedirs(f"{streamer_dir_root}/insights", exist_ok=True)

filename = f"{streamer_dir_root}/raw/RAW_{streamer}_{todays_date}_{time_of_trigger}.jsonl"
os.makedirs(os.path.dirname(filename), exist_ok=True)

with open(filename, 'a+') as f:
	chat = ChatDownloader().get_chat(url, inactivity_timeout=300)
	for message in chat:     
		f.write(json.dumps(message) + "\n")
		chat.print_formatted(message) #terminal check
	print(f"{streamer} is offline, done scraping")
	
#write file to raw WAITING FOR NAS
print("broke out of scrape test, write file to NAS here")

 
"""
this script generates a jsonl file, handle it like this:

	import pandas as pd    
	jsonObj = pd.read_json(path_or_buf=file_path, lines=True)

note the `lines=True` parameter, this handles jsonl
"""

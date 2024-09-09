from chat_downloader import ChatDownloader
from datetime import datetime
from time import sleep
from twitch_live_sensor import twitch_sensor_check
import json, os, random, shutil, sys

sys.path.append('../common')
from common_utils import init_streamer_files, write_to_store


streamer = (sys.argv[1]).lower() 
url = f"https://www.twitch.tv/{streamer}"

streamer_data = f"data/{streamer}"
streamer_store = f"/mnt/NASpipe/twitch/data/{streamer}"

### main:
# start live listener
# once live, generate files then start scrape, 
#   timeout will handle termination of scrape
# write to nas
while twitch_sensor_check(url) == False:
	print(f"{streamer} not live")
	sleep((29 + random.uniform(0, 5)))
	continue
	
print(f"{streamer} has gone live! Starting scrape")

filename = init_streamer_files(streamer)

with open(filename, 'a+') as f:
	chat = ChatDownloader().get_chat(url, inactivity_timeout=600)
	for message in chat:     
		f.write(json.dumps(message) + "\n")
		chat.print_formatted(message) #terminal check
	print(f"{streamer} is offline, done scraping")

print(f"scrape complete, writing {streamer}'s data into NAS:")

write_to_store("twitch", streamer, filename, "raw")


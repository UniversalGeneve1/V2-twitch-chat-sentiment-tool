from chat_downloader import ChatDownloader
from datetime import datetime
from time import sleep
from twitch_live_sensor import twitch_sensor_check
import json, multiprocessing, os, random, sys

streamer = sys.argv[1] 
url = f"https://www.twitch.tv/{streamer.lower()}"

#process components:
def scraper(stop_event):
	with open(filename, 'a+') as f:
		chat = ChatDownloader().get_chat(url)
		while not stop_event.is_set():
			for message in chat:     
				f.write(json.dumps(message) + "\n")
				chat.print_formatted(message) #terminal check
		print(f"{streamer} is offline, done scraping")

def stop_scrape_check(stop_event):
	cooldown_counter = 0
	flag = None
	while True:
		flag = twitch_sensor_check(url)
		if flag == True:
			cooldown_counter = 0
			sleep(180) # poll every 3 mins
			continue
		if cooldown_counter < 3:
			cooldown_counter += 1
			print(f"hit a snag, sensor cooldown {cooldown_counter} of 3")
			sleep(60)
			continue
		break
	stop_event.set()
	print("3 successive cooldowns hit, exiting scrape")
	
# Main process:
# when script is called, start infinite listener for live
# once live, begin multithread for end listener and scrape
# one offline, close file and write to raw.

while twitch_sensor_check(url) == False:
	print(f"{streamer} not live")
	sleep((13 + random.uniform(0, 5)))
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


# Start scraper + listener multiprocess
stop_event = multiprocessing.Event()

# Create and start the process for scrape
scrape = multiprocessing.Process(target=scraper, args=(stop_event,))
scrape.start()

# Call scrape_check and wait for stop event to generate
stop_scrape_check(stop_event)

# Wait for scrape to complete
scrape.terminate()

#write file to raw WAITING FOR NAS
print("broke out of scrape test, write file to NAS here")


"""
this script generates a jsonl file, handle it like this:

	import pandas as pd    
	jsonObj = pd.read_json(path_or_buf=file_path, lines=True)

note the `lines=True` parameter, this handles jsonl
"""

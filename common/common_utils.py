from datetime import datetime
import os, shutil

def init_streamer_files(streamer):
	
	todays_date = datetime.now().strftime('%Y-%m-%d')
	time_of_trigger = datetime.now().strftime('%H%M%S')
	streamer_dir_root = f"data/{streamer}"

	#make dirs and file
	os.makedirs(f"{streamer_dir_root}/preprocessed", exist_ok=True)
	os.makedirs(f"{streamer_dir_root}/insights", exist_ok=True)

	#handle jsonl files with pandas.read_json(..., lines=True)
	filename = f"{streamer_dir_root}/raw/RAW_{streamer}_{todays_date}_{time_of_trigger}.jsonl"
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	return filename
	
	

def write_to_store(platform, streamer, data, write_stage):
	#ensure dirs exist:
	
	if write_stage.lower() not in ['raw', 'preprocessed', 'insights']:
		raise ValueError("invalid write stage")
	
	nas_base_dir = "/mnt/NASpipe"
	os.makedirs(f"{nas_base_dir}/{platform}/{streamer}/raw", exist_ok=True)
	os.makedirs(f"{nas_base_dir}/{platform}/{streamer}/preprocessed", exist_ok=True)
	os.makedirs(f"{nas_base_dir}/{platform}/{streamer}/insights", exist_ok=True)
	
	# point to NAS in appropriate level
	destination = f"{nas_base_dir}/{platform}/{streamer}/{write_stage}"
	
	try:
		shutil.copy(data, destination)
		print(f"{data} moved successfully to {destination}")
	except Exception as e:
		print(f"Error moving file: {e}")

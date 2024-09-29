from datetime import datetime
from pathlib import Path
import os, shutil

stages = ['raw', 'preprocessed', 'insights']
nas_base_dir = "/mnt/NASpipe"	

#helper:
def init_file(fp):
	
	file_path = Path(fp)
	file_path.parent.mkdir(parents=True, exist_ok=True)
	file_path.touch(exist_ok=True)


def init_streamer_files(streamer, stages=stages):
	
	todays_date = datetime.now().strftime('%Y-%m-%d')
	time_of_trigger = datetime.now().strftime('%H%M%S')
	streamer_dir_root = f"data/{streamer}"

	#init all dirs, tracking files and raw write file
	for stage in stages:
		init_file(f"{streamer_dir_root}/{stage}/tracking.txt")
		
	raw_fn= f"{streamer_dir_root}/raw/RAW_{streamer}_{todays_date}_{time_of_trigger}.jsonl"
	
	return raw_fn
	
	
def ensure_dirs(write_stage, platform, streamer, nas_base_dir=nas_base_dir, stages=stages):
	
	if write_stage.lower() not in stages:
		raise ValueError("invalid write stage")
		
	for stage in stages:
		os.makedirs(f"{nas_base_dir}/{platform}/{streamer}/{stage}", exist_ok=True)
	
	
def write_to_store(platform, streamer, data, write_stage, stages=stages):
	
	ensure_dirs(write_stage, platform, streamer)

	# tracking file:
	trk_file = f"data/{streamer}/{write_stage}/tracking.txt"
	
	# point to NAS in appropriate level
	destination = f"{nas_base_dir}/{platform}/{streamer}/{write_stage}"
	
	# copy file into NAS
	try:
		shutil.copy(data, destination)
		print(f"{data} moved successfully to {destination}")
	except Exception as e:
		print(f"Error moving file: {e}")
		
	# add filename into tracking file:
	fname = data.rsplit("/", 1)[1]
	with open(f"data/{streamer}/{write_stage}/tracking.txt", "a+") as f:
		f.write(fname)
	
	# write tracking file into the storage
	try:
		shutil.copy(trk_file, destination)
		print(f"tracking file updated on NAS")
	except Exception as e:
		print(f"Error moving tracking file: {e}")
		

def read_files_to_process(input_stg, streamer, stages=stages):
	"""
		When a filename is written on its write_stage's tracking file, 
		it has been processed.
	"""
	ran_files = []
	
	with open(f"data/{streamer}/{input_stg}/tracking.txt", 'r') as ptf:
		for ln in ptf:
			ran_files.append(ln)

	return [f for f in os.listdir(f"data/{streamer}/{input_stg}") if f not in ran_files and f!= 'tracking.txt']
	
	
	































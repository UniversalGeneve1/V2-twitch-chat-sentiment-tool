from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os, sys

sys.path.append('../common')
from common_utils import write_to_store, read_files_to_process

"""
POA:
	- load csv files
	- generate time-series chart of average chat sentiment score vs time
		Q: what files are we creating to feed the website?
		  - might have to run this on a pi instead of an esp32.
		   	
  	- TODO: analyze using this algorithm:
	  - get the total unique chatters in a single stream.
	  - find 10% of the total unique chatters count
	  - find the average length of time in which the number of
		messages from unique chatters match the 
		10% value(round down).
		
		for example. we have 200 viewers, 10% is 20.
		find all time segments where 20 different chatters chat
		and find the average time length of those segments
		
		use that as the average time segment.
		
		^^ this needs to be part of processing
	      
	- generate top word count -> word cloud graph?
	
	- figure out how to use TPU as part of process
"""

streamer = (sys.argv[1]).lower() 
f2p = read_files_to_process('preprocessed', streamer)

for f in f2p:
	prc_csv = pd.read_csv(f)
	"""
	"""

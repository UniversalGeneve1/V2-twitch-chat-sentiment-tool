"""

	

"""


import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime, timedelta
import numpy as np

sys.path.append('../common')
from common_utils import write_to_store, read_files_to_process

"""
POA:
	- load csv files
	- generate time-series chart of average chat sentiment score vs time
  
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
"""


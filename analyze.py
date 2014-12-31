#!/usr/bin/env python 

import sys
import argparse
import logging
from modules import service_layer
import os

def parse_arguments(): 
	parser = argparse.ArgumentParser(description='Analyze sound file') 
	parser.add_argument("-b","--background", help="run process in background (does not work on windows machines)", action="store_true")
	parser.add_argument("-l","--local", help="use a local file", action="store_true")
	parser.add_argument("-gid","--guardian_ID", help="ID of the guardian", required=True)
	parser.add_argument("URL", help="URL to a wave file or path to a local file (see option -l)")
	
	return parser.parse_args()

def setup_logging(): 
	logger = logging.getLogger("services")
	logger.addHandler(logging.StreamHandler())  
	logger.addHandler(logging.FileHandler("logs/services.log"))
	# Todo: set logging level via config file / command line  
	logger.setLevel(level=logging.INFO)
	return logger

def main():
	args = parse_arguments() 
	logger = setup_logging() 

	# download / read sound file 
	aa = service_layer.AcquireAudio(logger)
	download_func = aa.read if args.local else aa.download
	sound = download_func(args.URL, args.guardian_ID)
	
	# fork if background option is set 
	if args.background and os.name != "nt": 
		newpid = os.fork()
		if newpid != 0: 
			# exit parent
			sys.os._exit(0)

	analyzer = service_layer.AnalyzeSound(logger)
	analyzer.analyze(sound)

	
if __name__ == "__main__":
	main()
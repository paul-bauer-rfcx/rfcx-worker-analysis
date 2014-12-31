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
	parser.add_argument("fp", help="File path to a Wav audio file", required=True)
	# TO DO: Need an encapsalation option to pass these in as well from Node app.
	# parser.add_argument('meta', type=file)
	# TO DO: IF the encapulatation method is NOT given: all flags required=True.
	# 		 ELSE ignore all manual meta flags
	parser.add_argument("-gid","--guardian_ID", help="ID of the guardian")
	parser.add_argument("-aid","--audio_ID", help="ID of the audio file")
	parser.add_argument("-t","--start_time", help="Local time audio recording started (ex. '2014-12-23T13:46:42.311Z').")
	parser.add_argument("-dur","--duration_ms", help="ID of the guardian")
	parser.add_argument("-lat","--latitude", help="ID of the guardian")
	parser.add_argument("-lon","--longitude", help="ID of the guardian")
	parser.add_argument("-amb","--ambientTemp", help="ID of the guardian")

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

	# read sound file from fs passed by sys.argv
	aa = service_layer.AcquireAudio(logger)
	sound = aa.read(args.URL, args.guardian_ID)

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

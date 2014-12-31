#!/usr/bin/env python

import sys
import argparse
import logging
from modules import service_layer
import os


def parse_arguments():
	parser = argparse.ArgumentParser(description='Analyze sound file')
	parser.add_argument("-b","--background", help="run process in background (does not work on windows machines)", action="store_true")
	parser.add_argument("-l","--local", help="Local development mode for write out locat, alerts, and files", action="store_true")
	parser.add_argument("file_path", help="File path to a Wav audio file")
	# Try to get data file with sound meta data before falling back to tags
	# try:
	# 	parser.add_argument("data_file", type=file, help="Meta-data file.")
	# except:
	parser.add_argument("-gid","--guardian_ID", help="ID of the guardian", required=True)
	parser.add_argument("-aid","--audio_ID", help="ID of the audio file")
	parser.add_argument("-t","--start_time", help="Local time audio recording started. ex.'2014-12-23T13:46:42.311Z'.")
	parser.add_argument("-dur","--duration_ms", help="ID of the guardian")
	parser.add_argument("-lat","--latitude", help="ID of the guardian")
	parser.add_argument("-lon","--longitude", help="ID of the guardian")
	parser.add_argument("-amb","--ambientTemp", help="ID of the guardian")

	return parser.parse_args()


def setup_logging(local=False):
	logger = logging.getLogger("services")
	logger.addHandler(logging.StreamHandler())
	logger.addHandler(logging.FileHandler("logs/services.log"))
	# Todo: set logging level via config file / command line
	if local:
		logger.setLevel(level=logging.DEBUG)
	else:
		logger.setLevel(level=logging.INFO)
	return logger


def main():
	args = parse_arguments()
	logger = setup_logging(args.local)

	# read sound file from fs passed by sys.argv
	aa = service_layer.AcquireAudio(logger)
	sound = aa.read(args.file_path, args.guardian_ID)

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

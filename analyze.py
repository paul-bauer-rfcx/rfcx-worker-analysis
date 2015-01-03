#!/usr/bin/env python

import sys
import argparse
import logging
import logging.config
from modules import service_layer
import os
import json

# try importing Environmental Variable from file
try:
	# DEVELOPMENT
	with open('./env_var_override.properties', 'r') as f:
		for line in f:
			tmp = [x.strip() for x in line.split("=")]
			tmp[0] = tmp[1]
except ImportError:
	# PRODUCTION
	pass

def parse_arguments():
	parser = argparse.ArgumentParser(description='Analyze sound file')
	parser.add_argument("-b","--background", help="run process in background (does not work on windows machines)", action="store_true")
	parser.add_argument("-l","--local", help="Local development mode for write out locat, alerts, and files", action="store_true")
	parser.add_argument("file_path", help="File path to a Wav audio file")
	# Try to get meta-data from a file before falling back to flags
	try:
		parser.add_argument("data_file", type=file, help="Meta-data file.")
	except:
		parser.add_argument("-g","--guardian_id", help="ID of the guardian", required=True)
		parser.add_argument("-a","--audio_id", help="ID of the audio file", required=True)
		parser.add_argument("-dt","--start_time", help="Local time audio recording started. ex.'2014-12-23T13:46:42.311Z'.", required=True)
		parser.add_argument("-ll","--lat_lng", help="Lat/Long of device", required=True)
		parser.add_argument("-t","--ambient_temp", help="Ambient temp", required=True)
	return parser.parse_args()

def parse_data_file(args):
	meta_data = {}
	if args.data_file:
		# parse the data file passed for args
		for line in args.data_file:
			tmp = [x.strip() for x in line.split("=")]
			if tmp[0] in ["lat_lng"]:
				tmp[1] = tmp[1].split(",")
			meta_data[tmp[0]] = tmp[1]
	else:
		# collect manually given flag agrs
		meta_data["guardian_id"] = args.guardian_id
		meta_data["audio_id"] = args.audio_id
		meta_data["start_time"] = args.start_time
		meta_data["lat_lng"] = args.lat_lng.split(",")
		meta_data["ambient_temp"] = args.ambient_temp
	return meta_data

def setup_logging(local=False):
	logger = logging.getLogger("services")
	# load logging settings
	logging.config.fileConfig('logging.conf')
	# Todo: set logging level via config file / command line
	if local:
		logger.setLevel(level=logging.DEBUG)
	else:
		logger.setLevel(level=logging.INFO)
	return logger


def main():
	args = parse_arguments()
	meta_data = parse_data_file(args)
	logger = setup_logging(args.local)

	# read sound file from fs passed by sys.argv
	aa = service_layer.AcquireAudio(logger)
	sound = aa.read(args.file_path, meta_data)

	# fork if background option is set
	if args.background and os.name != "nt":
		newpid = os.fork()
		if newpid != 0:
			# exit parent
			exit(0)

	analyzer = service_layer.AnalyzeSound(logger)
	analyzer.analyze(sound)
	exit(0)

if __name__ == "__main__":
	main()

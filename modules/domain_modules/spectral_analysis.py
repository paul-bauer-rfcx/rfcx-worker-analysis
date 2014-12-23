# extraction and analysis module
import scipy
from scipy.io import wavfile
import numpy as np

class Spectrum:
	def __init__(self):
		'''Spectrum Class: Defines the properties and form that output spectrum data should take.'''
		pass

class SpectralAnalysis: 
	def __init__(self, file_path, analysis="welch"):
		'''Spectral Analysis Class:
		Takes in a file path to audio clip, analysis method desired. '''
		self.analysis = analysis
		self.spectrum = self.select_analysis()

	def select_analysis(self):
		if self.analysis == 'welch':
			# return self.welch()
			return Spectrum()
		else:
			# throw error 
			raise Exception("Analysis type selected was not found.")

	def welch(self):
		''' Function will process an audio sample in intervals defined 
		by the step parameter and output frequency spectrum data as 
		a tuple (freq, power) for each. 
		Function outputs a list with all snippet tuples. '''
		# Default settings for Welch analysis
		snd=self.sound[0]
		step = 1000,
		fft_size = 500
		overlap = 250
		max_bin = snd.shape[0]-self.step
		start_bin = 0
		freqSpect = []
		# step over the numpy array and process the audio
		while start_bin < max_bin:
			snippet = snd[start_bin:(start_bin+self.step)]
			start_bin += self.step
			freqSpect.append(scipy.signal.welch(snippet, fs=self.sound[1], window=self.window, nperseg=fft_size, noverlap=overlap, return_onesided=True))
		return freqSpect

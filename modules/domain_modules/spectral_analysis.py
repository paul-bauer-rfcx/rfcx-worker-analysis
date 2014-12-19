# extraction and analysis module
import sndfileio 
import scipy
import numpy as np

class SpectralAnalysis: 
	def __init__(self, step=1000, fft_size=500, overlap=250, window='hanning'): 
		self.step = step 
		self.fft_size = fft_size
		self.overlap = overlap
		self.window = window 

	def extract(self, path):
		''' Function will process an audio sample in intervals defined 
		by the step parameter and output frequency spectrum data as 
		a tuple (freq, power) for each. 
		Function outputs a list with all snippet tuples. '''
		snd, fs = sndfileio.sndread(path)
		max_bin = snd.shape[0]-self.step
		start_bin = 0
		freqSpect = []
		# step over the numpy array and process the audio
		while start_bin < max_bin:
			snippet = snd[start_bin:(start_bin+self.step)]
			start_bin += self.step
			freqSpect.append(self.analyze(snippet, fs))
		return freqSpect

	def analyze(self, snd, fs): 
		return scipy.signal.welch(snd, fs=fs, window=self.window, nperseg=self.fft_size, noverlap=self.overlap, return_onesided=True) 

import librosa as lib
import numpy as np
from pygame import mixer

def load():
	y, sr = lib.load('kanye.wav')
	# 256 sample window should be used to get frequency windows about 256 / 22050 Hz = 0,01161 s about 12 ms long
	f = lib.amplitude_to_db(np.abs(lib.stft(y, hop_length=256, win_length=2048))) # Equal hop length and window length to get an even division of the buffer
	yMax = max(y)
	yMin = min(y)

	y_ms = round(y.shape[0] / sr) * 1000 # Song length in ms
	a_list = []
	df_list = []

	for t in range(0,  y_ms, 12):
		a, df = handle(y, yMax, yMin, f, t) # Get normalized frequency and dominating frequency
		a_list.append(a)
		df_list.append(df)

	return a_list, df_list

# Calculate and return the average amplitude and the dominating frequency of the sample window
def handle(y, yMax, yMin, f, t):
	sr = 22050 # Librosas sample rate
	sampleLength = 256 # Chosen samples per window in stft
	currentFrameNr = round(t / 12) # Since each frame is 12 ms
	maxSampledFrequency = (sr / 2) # Nyquist theorem
	frequenciesPerBand = round( maxSampledFrequency / f.shape[0]) # Nr of frequencies per band in the stft

	# Do nothing if out of bounds
	if (currentFrameNr >= f.shape[1]):
		return

	currentFrame = f[:, currentFrameNr]
	
	dominatingFrequencies = []
	# Get five most dominating frequencies
	for i in range(0, 5):
		frequencyBandNr = np.where(currentFrame == max(currentFrame)) # Get frequency band index with largest magnitude
		frequencyBandNr = frequencyBandNr[0][0] # Convert from 1D array to scalar
		dominatingFrequency = round( (frequencyBandNr * frequenciesPerBand) + (frequenciesPerBand / 2) ) # Step into the middle of the dominating frequency band
		dominatingFrequencies.append(dominatingFrequency)
		currentFrame[frequencyBandNr] = 0
	
	avgDominatingFrequency = sum(dominatingFrequencies) / len(dominatingFrequencies)
	gamma = 1 # Larger gamma = more contrast 
	normalizedDominatingFrequency = (np.log(avgDominatingFrequency) / np.log(maxSampledFrequency)) # To get normalized value
	normalizedDominatingFrequency = normalizedDominatingFrequency ** (1 / gamma)  # Gamma correction to increase difference in frequencies

	ampWindowStart = round( ((22050) / 1000) * t )
	currentAmplitudeWindow = y[ampWindowStart: (ampWindowStart + sampleLength)]
	averageAmplitude = sum(currentAmplitudeWindow) / sampleLength
	normalizedAverageAmplitude = (averageAmplitude - yMin) / (yMax - yMin) # Scale to (0, 1)
	return normalizedAverageAmplitude, normalizedDominatingFrequency

# To play audio file, uses pygames mixer
def play(song):
	mixer.init()
	mixer.music.load(song)
	mixer.music.set_volume(0.5)
	mixer.music.play()





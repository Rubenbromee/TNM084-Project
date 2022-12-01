import librosa as lib
import numpy as np

def load():
	y, sr = lib.load('song.wav')
	# 256 sample window should be used to get frequency windows about 256 / 22050 Hz = 0,01161 s about 12 ms long
	f = np.abs(lib.stft(y, hop_length=256, win_length=256)) # Equal hop length and window length to get an even division of the buffer
	yMax = max(y)
	yMin = min(y)

	frequenciesPerBand = round( (sr / 2) / f.shape[0])
	fMaxIdx = np.where(f == f.max()) # Look for the indicies with the largest value
	fMinIdx = np.where(f == np.min(f[np.nonzero(f)])) # Look for indicies with the smallest non-zero value
	print('fMaxIdx', fMaxIdx)
	print('fMinIdx', fMinIdx)
	fMax = 10000 #round( ( * ) + (frequenciesPerBand / 2) )
	fMin = 10

	return y, yMax, yMin, f, fMax, fMin

# Calculate and return the average amplitude and the dominating frequency of the sample window
def handle(y, yMax, yMin, f, fMax, fMin, t):
	sr = 22050 # Librosas sample rate
	sampleLength = 256
	#fMax = 
	currentFrameNr = round(t / 12)
	frequenciesPerBand = round( (sr / 2) / f.shape[0])

	# Do nothing if out of bounds
	if (currentFrameNr >= f.shape[1]):
		return

	currentFrame = f[:, currentFrameNr]
	frequencyBandNr = np.where(currentFrame == max(currentFrame)) # Get frequency band index with largest amplitude
	frequencyBandNr = frequencyBandNr[0][0] # Convert from 1D array to scalar
	dominatingFrequency = round( (frequencyBandNr * frequenciesPerBand) + (frequenciesPerBand / 2) ) # Step into the middle of the dominating frequency band
	scaledDominatingFrequency = (dominatingFrequency - fMin) / (fMax - fMin)

	ampWindowStart = round( ((22050) / 1000) * t )
	currentAmplitudeWindow = y[ampWindowStart: (ampWindowStart + sampleLength)]
	averageAmplitude = sum(currentAmplitudeWindow) / sampleLength
	scaledAverageAmplitude = (averageAmplitude - yMin) / (yMax - yMin) # Scale to (0, 1)
	return scaledAverageAmplitude, scaledDominatingFrequency
	


y, yMax, yMin, f, fMax, fMin = load()
a, df = handle(y, yMax, yMin, f, fMax, fMin, 5000)
print("Amplitude:", a, "Dominating frequency:", df)





import numpy as np
import pyaudio
import wave
from pydub import AudioSegment
from pydub.playback import play
import time

np.set_printoptions(suppress=True)  # don't use scientific notation

CHUNK = 4096  # number of data points to read at a time
RATE = 44100  # time resolution of the recording device (Hz)
CHANNELS = 1
FORMAT = pyaudio.paInt16

p = pyaudio.PyAudio()  # start the PyAudio class

# uses default input device
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                input=True, frames_per_buffer=CHUNK)
number = 1.0  # increasing the rate of number range falls
frames = []
freqArray = []


def analyze():
    """Analyzes audio input and writes peak frequencies into array."""
    # create a numpy array holding a single read of audio data
    try:
        while True:
            data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
            # smooth the FFT by windowing data
            data = data * np.hanning(len(data))
            fft = abs(np.fft.fft(data).real)
            fft = fft[:int(len(fft) / 2)]  # keep only first half
            freq = np.fft.fftfreq(CHUNK, number / RATE)
            freq = freq[:int(len(freq) / 2)]  # keep only first half
            freqPeak = freq[np.where(fft == np.max(fft))[0][0]] + 1
            #print("peak frequency: %d Hz" % freqPeak)
            data2 = stream.read(CHUNK)
            frames.append(data2)
            freqArray.append(int(freqPeak))
    except KeyboardInterrupt:
        # close the stream gracefully
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open("output.wav", 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
t0 = time.perf_counter()
analyze()
t1 = time.perf_counter()
print(freqArray)
elapsed = t1 - t0
print(f'Time: {elapsed}')
print(elapsed / len(freqArray))
# play(AudioSegment.from_wav("output.wav"))

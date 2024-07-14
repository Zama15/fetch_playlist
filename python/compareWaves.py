import numpy as np
import os.path as path
import matplotlib.pyplot as plt
import wave
import tabulate

ROOT = path.dirname(path.abspath(__file__))
TITLE_MV = 'BIBBIDIBA.wav'
TITLE_LIVE = 'BIBBIDIBALiveAnniversary.wav'

# ========= MV =========
audioOriginal = wave.open(path.join(ROOT, TITLE_MV), 'r')

# Read the audio file as a byte and convert it to a numpy array
originalByte = audioOriginal.readframes(-1)
originalArray = np.frombuffer(originalByte, dtype=np.int16)

# Get the sample rate of the audio file and calculate the duration in minutes
originalSampleRate = audioOriginal.getframerate()
originalduration = len(originalArray) / originalSampleRate

# Find the sound waves originalTimestamp
originalTimestamp = np.linspace(0, originalduration, len(originalArray))

# ========= Live =========
audioLive = wave.open(path.join(ROOT, TITLE_LIVE), 'r')

# Read the audio file as a byte and convert it to a numpy array
liveByte = audioLive.readframes(-1)
liveArray = np.frombuffer(liveByte, dtype=np.int16)

# Get the sample rate of the audio file and calculate the duration in minutes
liveSampleRate = audioLive.getframerate()
liveduration = len(liveArray) / liveSampleRate

# Find the sound waves originalTimestamp
liveTimestamp = np.linspace(0, liveduration, len(liveArray))

# ========= Print =========
head = ['', 'MV', 'Live']
data = [
    ['Sample rate', originalSampleRate, liveSampleRate],
    ['Duration(m)', f"{(originalduration / 60):.2f}", f"{(liveduration / 60):.2f}"],
    ['Audio data lenght', len(originalArray), len(liveArray)]
]

print(tabulate.tabulate(data, headers=head, tablefmt='fancy_grid'))

# ========= Plot =========
# Get a snippet of the audio file
secondsInit = 0
secondsEnd = 30

originalTimestampSnippet = originalTimestamp[secondsInit * originalSampleRate:secondsEnd * originalSampleRate]
originalArraySnippet = originalArray[secondsInit * originalSampleRate:secondsEnd * originalSampleRate]

liveTimestampSnippet = liveTimestamp[secondsInit * liveSampleRate:secondsEnd * liveSampleRate]
liveArraySnippet = liveArray[secondsInit * liveSampleRate:secondsEnd * liveSampleRate]

plt.title(f"{TITLE_MV} vs {TITLE_LIVE} - {secondsInit}s to {secondsEnd}s")
plt.xlabel('Time(s)')
plt.ylabel('Amplitude')
plt.plot(originalTimestampSnippet, originalArraySnippet, label=TITLE_MV, alpha=0.7)
plt.plot(liveTimestampSnippet, liveArraySnippet, label=TITLE_LIVE, alpha=0.7)
plt.legend()
plt.show()

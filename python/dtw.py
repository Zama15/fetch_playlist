import librosa
import numpy as np
import os.path as path
import matplotlib.pyplot as plt

ROOT = path.dirname(path.abspath(__file__))
TITLE_MV = 'BIBBIDIBA.wav'
TITLE_LIVE = 'BIBBIDIBALiveAnniversary.wav'

y, sr = librosa.load(path.join(ROOT, TITLE_MV))
y2, sr2 = librosa.load(path.join(ROOT, TITLE_LIVE))

# sTime = 0
# eTime = 1

# sFrameOriginal = librosa.time_to_samples(sTime, sr=sr)
# eFrameOriginal = librosa.time_to_samples(eTime, sr=sr)

# sFrameLive = librosa.time_to_samples(sTime, sr=sr2)
# eFrameLive = librosa.time_to_samples(eTime, sr=sr2)

# === RMSE ===

# rmse = librosa.feature.rms(y=y)

# plt.figure(figsize=(10, 4))
# plt.title(f"{TITLE_MV} - RMSE")
# plt.plot(rmse[0])
# plt.tight_layout()
# plt.show()

# === Onset ===
# oncentOriginal = librosa.onset.onset_strength(y=y, sr=sr)
# oncentOriginalFragment = oncentOriginal[sFrameOriginal:eFrameOriginal]
# timeFragmentOriginal = librosa.frames_to_time(range(len(oncentOriginalFragment)), sr=sr)

# oncentLive = librosa.onset.onset_strength(y=y2, sr=sr2)
# oncentLiveFragment = oncentLive[sFrameLive:eFrameLive]
# timeFragmentLive = librosa.frames_to_time(range(len(oncentLiveFragment)), sr=sr2)

# plt.figure(figsize=(10, 4))
# plt.title(f"{TITLE_MV} - Onset")
# plt.plot(timeFragmentOriginal, oncentOriginalFragment, label='MV', alpha=0.7)
# plt.plot(timeFragmentLive, oncentLiveFragment, label='Live', alpha=0.7)
# plt.tight_layout()
# plt.show()

# === Waveform ===
plt.figure(figsize=(10, 4))
plt.title(f"{TITLE_MV} vs {TITLE_LIVE}")
plt.plot(y, label='MV', alpha=0.7)
plt.plot(y2, label='Live', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

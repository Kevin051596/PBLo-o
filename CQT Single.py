import librosa
import librosa.display
from matplotlib import pyplot as plt
import numpy as np
from pydub.audio_segment import AudioSegment

#導入音檔
y, sr = librosa.load("D:\PBL\C42.wav",22050,duration=1.0)
#設定網格
fig, ax = plt.subplots()
#製圖
img = librosa.display.specshow(librosa.amplitude_to_db(librosa.cqt(y,sr=16000),ref=np.max),
                               sr=sr, x_axis='time', y_axis='cqt_note', ax=ax)
ax.set_title(' Piano spectrum')
#fig.colorbar(img, ax=ax, format="%+2.0f dB")
#屬性設置怪怪的

plt.show()
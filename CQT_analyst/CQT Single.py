import librosa
import librosa.display
from matplotlib import pyplot as plt
import numpy as np
from playsound import playsound
 
#導入音檔
y, sr = librosa.load('D:\PBL\music_3.wav',44100,duration=3)
#設定網格
fig, ax = plt.subplots()
#製圖
CQT = librosa.amplitude_to_db(librosa.cqt(y,sr=sr),ref=np.max)
#CQT = librosa.amplitude_to_db(librosa.stft(y, n_fft=512, win_length=512, hop_length=256, center=True),ref=np.max)
img = librosa.display.specshow(CQT,sr=sr, x_axis='time', y_axis='cqt_note', ax=ax)
#ax.set_title(' C4-C5 spectrum')
#fig.colorbar(img, ax=ax, format="%+2.0f dB")
#屬性設置怪怪的
#fig.colorbar(img, ax=ax, format="%+2.0f dB")

plt.show()

print(CQT)

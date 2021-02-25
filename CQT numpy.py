import librosa
import librosa.display
from matplotlib import pyplot as plt
import numpy as np
from playsound import playsound
 
playsound('piano-C4.wav')

#導入音檔
y, sr = librosa.load("D:\PBL\5.wav",22050)
#設定網格
fig, ax = plt.subplots()
#製圖
CQT = np.abs(librosa.cqt(y,sr=sr))
img = librosa.display.specshow(librosa.amplitude_to_db(CQT, ref=np.max),sr=sr, x_axis='time', y_axis='cqt_note', ax=ax)
ax.set_title('Flute-C4 spectrum')
#fig.colorbar(img, ax=ax, format="%+2.0f dB")

plt.show()

print(CQT)

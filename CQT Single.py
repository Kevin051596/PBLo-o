import librosa
import librosa.display
from matplotlib import pyplot as plt
import numpy as np
from playsound import playsound
 
#playsound('piano-C4.wav')


#導入音檔
y, sr = librosa.load("D:\PBL\Flute-C4.wav",22050,duration=2.0)
#設定網格
fig, ax = plt.subplots()
#製圖
CQT = librosa.amplitude_to_db(librosa.cqt(y,sr=sr),ref=np.max)
img = librosa.display.specshow(CQT,sr=sr, x_axis='time', y_axis='cqt_note', ax=ax)
ax.set_title(' Flute-C4 spectrum')
#fig.colorbar(img, ax=ax, format="%+2.0f dB")
#屬性設置怪怪的

plt.show()
print(CQT)

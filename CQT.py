import librosa
import librosa.display
from matplotlib import pyplot as plt
import numpy as np
from pydub import AudioSegment
import wave

'''
sound = AudioSegment.from_wav("D:\PBL\TESTA1.wav")
f = wave.open("TESTA1.wav",'wb')
f.setnchannels(1)   # 频道数
f.setsampwidth(2)   # 量化位数
f.setframerate(16000)   # 取样频率
f.setnframes(len(sound._data))   # 取样点数，波形数据的长度
f.writeframes(sound._data)   # 写入波形数据
f.close()
'''

#導入音檔
y=[0]*6
y[0],sr = librosa.load("D:\PBL\TESTF2.wav",22050,duration=11.0)
y[1],sr = librosa.load("D:\PBL\TESTF3.wav",22050,duration=11.0)
y[2],sr = librosa.load("D:\PBL\TESTF4.wav",22050,duration=11.0)
y[3],sr = librosa.load("D:\PBL\TESTF5.wav",22050,duration=11.0)
y[4],sr = librosa.load("D:\PBL\TESTF6.wav",22050,duration=11.0)
y[5],sr = librosa.load("D:\PBL\TESTF7.wav",22050,duration=11.0)



#設定網格
fig,ax =plt.subplots(nrows=2,ncols=4,sharex=True, sharey=True,figsize=(15,15))

#CQT分析
CQT=[0]*6
k=0
j=0
for i in range(6):
    CQT[i] = librosa.amplitude_to_db(librosa.cqt(y[i],sr=16000),ref=np.max)
    img =librosa.display.specshow(CQT[i],x_axis='time',y_axis='cqt_note',ax=ax[j,k])
    fig.colorbar(img,ax=ax[j,k],format="%+2.0f dB")
    ax[j,k].set(title='Constant-Q F{}'.format(i+2))
    ax[j,k].set(ylabel='CQT')
    if(k==3): 
        k=0 
        j+=1
    else: 
        k+=1
        
#調整圖距
fig.tight_layout()
plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.2, 
                    hspace=0.35)
plt.show()
import librosa
import librosa.display
from matplotlib import pyplot as plt
import numpy as np
from pydub import AudioSegment
import wave
from playsound import playsound

playsound('C3-C4.wav')

#導入音檔
y=[0]*4
sr=[0]*4
y[0],sr[0] = librosa.load("D:\PBL\C3-C4_p.wav",22050,duration=3.0)
y[1],sr[1] = librosa.load("D:\PBL\C3-C4_p.wav",44100,duration=3.0)
y[2],sr[2] = librosa.load("D:\PBL\C3-C4_p.wav",88200,duration=3.0)
y[3],sr[3] = librosa.load("D:\PBL\C3-C4_p.wav",132300,duration=3.0)
#y[4],sr = librosa.load("D:\PBL\TESTF6.wav",22050,duration=11.0)
#y[5],sr = librosa.load("D:\PBL\TESTF7.wav",22050,duration=11.0)



#設定網格
fig,ax =plt.subplots(nrows=2,ncols=2,sharex=True, sharey=True,figsize=(15,15))

#CQT分析
CQT=[0]*4
k=0
j=0
for i in range(4):
    CQT[i] = librosa.amplitude_to_db(librosa.cqt(y[i],sr=sr[i]),ref=np.max)
    img =librosa.display.specshow(CQT[i],sr=sr[i],x_axis='time',y_axis='cqt_note',ax=ax[j,k])
    #fig.colorbar(img,ax=ax[j,k],format="%+2.0f dB")
    ax[j,k].set(title='Constant-Q F{}'.format(i+2))
    ax[j,k].set(ylabel='CQT')
    if(k==1): 
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
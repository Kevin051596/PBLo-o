import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import librosa

# Load an example with vocals.
y, sr = librosa.load('001.mp3', sr=44100)  # 加載liborsa音檔；duration：從第幾秒後開始擷取

# And compute the spectrogram magnitude and phase
S_full, phase = librosa.magphase(librosa.stft(y))  # 取得[幅度、相位]特徵

fig, ax = plt.subplots(nrows=2, sharex=True, sharey=True)
img = librosa.display.specshow(librosa.amplitude_to_db(S_full, ref=np.max),
                               y_axis='log', x_axis='time', sr=sr, ax=ax[0])  # 繪製光譜圖

fig.colorbar(img, ax=ax[0])  # 繪製光譜圖
ax[0].set(title='Original Spectrum')
ax[0].label_outer()

S_filter = librosa.decompose.nn_filter(S_full, aggregate=np.median, metric='cosine',
                                       width=int(librosa.time_to_frames(2, sr=sr)))  #相近點合併
S_filter = np.minimum(S_full,S_filter)

margin_i, margin_v = 2, 10
power = 2

mask_i = librosa.util.softmask(S_filter,
                               margin_i * (S_full - S_filter),
                               power=power)

mask_v = librosa.util.softmask(S_full - S_filter,
                               margin_v * S_filter,
                               power=power)

S_foreground = mask_v * S_full
S_background = mask_i * S_full

img = librosa.display.specshow(librosa.amplitude_to_db(S_foreground, ref=np.max),
                         y_axis='log', x_axis='time', sr=sr, ax=ax[1])
ax[1].set(title='foreground')
fig.colorbar(img, ax=ax[1])

fig.tight_layout()
plt.subplots_adjust(wspace =0, hspace =0.3)
plt.show()

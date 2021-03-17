import os
import shutil
import librosa
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['svg.fonttype'] = 'none'
import numpy as np
from scipy.io.wavfile import read as readwav
from matplotlib import animation
import matplotlib as mpl
from matplotlib import cm
from collections import OrderedDict
import librosa.display
import pandas
import console

# Constants
n_fft = 512
hop_length = 256
SR = 16000
over_sample = 4
res_factor = 0.8
octaves = 6
notes_per_octave=5
min = 0.34
cmaps = OrderedDict()
cmaps['Miscellaneous'] = ['rainbow']
k=1

# Plotting functions
cdict  = {
          'red':  ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'green': ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'alpha':  ((0.0, 1.0, 1.0),
                   (1.0, 0.0, 0.0))
        }
my_mask = matplotlib.colors.LinearSegmentedColormap('MyMask', cdict)
plt.register_cmap(cmap=my_mask)


def animation_specgram(path, peak=70.0, use_cqt=True):
  # Add several samples together
  '''
  if isinstance(path, list):
    for i, p in enumerate(path):
      sr, a = readwav(f)
      audio = a if i == 0 else a + audio
  # Load one sample
  else:  
    '''  
  #sr, audio = readwav(path)
  fig ,ax = plt.subplots()
  audio, sr = librosa.load(path,44100,duration= 10)
  audio = audio.astype(np.float)
  if use_cqt:
    C = librosa.cqt(audio, sr=sr, hop_length=hop_length, 
                      bins_per_octave=int(notes_per_octave*over_sample), 
                      n_bins=int(octaves * notes_per_octave * over_sample), 
                      filter_scale=res_factor, 
                      fmin=librosa.note_to_hz('C2')
                      )
  else:
    C = librosa.stft(audio, n_fft=n_fft, win_length=n_fft, hop_length=hop_length, center=True)
  mag, phase = librosa.core.magphase(C)
  phase_angle = np.angle(phase)
  phase_unwrapped = np.unwrap(phase_angle)
  dphase = phase_unwrapped[:, 1:] - phase_unwrapped[:, :-1]
  dphase = np.concatenate([phase_unwrapped[:, 0:1], dphase], axis=1) / np.pi
  mag = (librosa.power_to_db(mag ** 2, amin=1e-13, top_db=peak, ref=np.max) / peak) + 1
  mag[mag < min] = 0.2
  return mag, ax, fig

def animat(path):  
  def animate(i):
    im1.set_data(update_data(array,i))
    im2.set_data(update_data(array,i))
    return im1, im2
  def genearate_data(n):
    data = n[:: -1, 0 : 120]
    return data
  def update_data(n,i):
    data = n[:: -1, i:(i+120)]
    return data

  array,ax,fig = animation_specgram(path)
  im1 = ax.matshow(genearate_data(array), cmap=plt.cm.get_cmap('rainbow'))  
  im2 = ax.matshow(genearate_data(array), cmap=my_mask)
  plt.yticks([20,40,60,80,100],['C7','C6','C5','C4','C3'])
  ax.xaxis.set_visible(False)
  ani = animation.FuncAnimation(fig, animate, frames=1600, interval=10, save_count=10)
  console.discription()
  console.animation_output(path, ani)
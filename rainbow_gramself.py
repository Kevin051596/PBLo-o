import os
import librosa
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['svg.fonttype'] = 'none'
import numpy as np
import matplotlib as mpl
from matplotlib import cm
from collections import OrderedDict
import librosa.display
import pandas
import console
import shutil

# Constants
n_fft = 512
hop_length = 256
SR = 16000
over_sample = 4
res_factor = 0.8
octaves = 6
notes_per_octave=5
min = 0.34

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


def note_specgram(path, peak=70.0, use_cqt=True,showdata=False):

  fig ,ax = plt.subplots()
  audio, sr = librosa.load(path,44100,duration= 3)
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
  cax = ax.matshow(mag[:-1 , ::], cmap=plt.cm.get_cmap('rainbow'))
  cax = ax.matshow(mag[: -1, :], cmap=my_mask)

  plt.yticks([20,40,60,80,100],['C7','C6','C5','C4','C3'])
  ax.xaxis.set_visible(False)
  
  console.discription()
  console.newspectrum(path, fig)
  if showdata:
    console.xlsx(mag, path)
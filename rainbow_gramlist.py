import os
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


def show_sample(list):
    print(list)
    df = pandas.DataFrame(data=list)
    df.to_excel("test0.35.xlsx")

def note_specgram(path, ax, i, peak=70.0, use_cqt=True):
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
  if (i+1)%2 == 0 : 
    ax.matshow(mag[:: -1, :], cmap=plt.cm.get_cmap('brg'))
  else :
    ax.matshow(mag[:: -1, :], cmap=plt.cm.get_cmap('rainbow'))   
  ax.matshow(mag[:: -1, :], cmap=my_mask)
  #show_sample(mag)

def plot_notes(list_of_paths, rows=2, cols=1, col_labels=[], row_labels=[],
              use_cqt=True, peak=70.0):
  """Build a CQT rowsXcols.
  """
  column = 0
  N = len(list_of_paths)
  try:
    assert N == rows*cols
  except AssertionError:
    print ('N != rows*col')
  fig, axes = plt.subplots(rows, cols, figsize=(10, 4.5), sharex='col', sharey='row')
  fig.subplots_adjust(left=0.1, right=0.9, wspace=0.05, hspace=0.1)
  
  for i, path in enumerate(list_of_paths):
    row = (int)(i / cols)
    col = (int)(i % cols)
    if rows == 1:
      ax = axes[col]
    elif cols == 1:
      ax = axes[row]
    else:
      ax = axes[row, col]
    
    print (row, col, path, ax, peak, use_cqt)
    note_specgram(path, ax, i, peak, use_cqt)
    
    ax.set_facecolor('white')
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['C7', 'C6', 'C5', 'C4', 'C3'])
    ax.set_xticks([])
    if col == 0 and row_labels:
      ax.set_ylabel(row_labels[row])
    if row == rows-1 and col_labels:
      ax.set_xlabel(col_labels[col])

  fig.savefig('C5-C6_compare.png')
    

   
  
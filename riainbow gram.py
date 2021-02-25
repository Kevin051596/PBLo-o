import os
import librosa
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['svg.fonttype'] = 'none'
import numpy as np
from scipy.io.wavfile import read as readwav

# Constants
n_fft = 512
hop_length = 256
SR = 16000
over_sample = 4
res_factor = 0.8
octaves = 6
notes_per_octave=5

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

def note_specgram(path, ax, peak=70.0, use_cqt=True):
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
  audio, sr = librosa.load(path,22050)
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
  #mag = (librosa.logamplitude(mag**2, amin=1e-13, top_db=peak, ref_power=np.max) / peak) + 1
  mag = (librosa.power_to_db(mag ** 2, amin=1e-13, top_db=peak, ref=np.max) / peak) + 1
  ax.matshow(mag[::-1, :], cmap=plt.cm.rainbow)
  ax.matshow(mag[::-1, :], cmap=my_mask)

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
  fig, axes = plt.subplots(rows, cols, sharex=True, sharey=True)
  fig.subplots_adjust(left=0.1, right=0.9, wspace=0.05, hspace=0.1)

  #fig = plt.figure(figsize=(18, N * 1.25))
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
    note_specgram(path, ax, peak, use_cqt)
    
    ax.set_facecolor('white')
    ax.set_xticks([]); ax.set_yticks([])
    if col == 0 and row_labels:
      ax.set_ylabel(row_labels[row])
    if row == rows-1 and col_labels:
      ax.set_xlabel(col_labels[col])

if __name__ == "__main__":
  fig, axes = plt.subplots(2,1,sharex ='col',sharey ='row')
  list_1 = ['D:\PBL\Test_fr002\piano-C6.wav','D:\PBL\music_3.wav']
  plot_notes(list_1)
  plt.show()
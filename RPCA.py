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
import math
import numpy.linalg
from ipython_genutils.py3compat import xrange

# Constants
n_fft = 512
hop_length = 256
SR = 16000
over_sample = 4
res_factor = 0.8
octaves = 6
notes_per_octave=5
min = 0.7
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
    df.to_excel("RPCAmusic_3.xlsx")

def robust_pca(M):
    L = numpy.zeros(M.shape)
    S = numpy.zeros(M.shape)
    Y = numpy.zeros(M.shape)
    print(M.shape)
    mu = (M.shape[0] * M.shape[1]) / (4.0 * L1Norm(M))
    lamb = max(M.shape) ** -0.5
    while not converged(M,L,S):
        L = svd_shrink(M - S - (mu**-1) * Y, mu)
        S = shrink(M - L + (mu**-1) * Y, lamb * mu)
        Y = Y + mu * (M - L - S)
    return L,S
    
def svd_shrink(X, tau):
    U,s,V = numpy.linalg.svd(X, full_matrices=False)
    return numpy.dot(U, numpy.dot(numpy.diag(shrink(s, tau)), V))
    
def shrink(X, tau):
    V = numpy.copy(X).reshape(X.size)
    for i in xrange(V.size):
        V[i] = math.copysign(max(abs(V[i]) - tau, 0), V[i])
        if V[i] == -0:
            V[i] = 0
    return V.reshape(X.shape)
            
def frobeniusNorm(X):
    accum = 0
    V = numpy.reshape(X,X.size)
    for i in xrange(V.size):
        accum += abs(V[i] ** 2)
    return math.sqrt(accum)

def L1Norm(X):
    return max(numpy.sum(X,axis=0))

def converged(M,L,S):
    error = frobeniusNorm(M - L - S) / frobeniusNorm(M)
    print ("error =", error)
    return error <= 10e-6

def note_specgram(path, peak=70.0, use_cqt=True):
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
  magL, magS = robust_pca(mag)
  magS /= 100
  magS[magS < min] = 0.2
  ax.matshow(magS[:: -1, :], cmap=plt.cm.get_cmap('rainbow'))   
  ax.matshow(magS[:: -1, :], cmap=my_mask)
  plt.yticks([20,40,60,80,100],['C7','C6','C5','C4','C3'])
  ax.xaxis.set_visible(False)
  show_sample(magS)

  fig.savefig('C4-C5_p-all.png')

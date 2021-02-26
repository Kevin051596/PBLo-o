from rainbow_gram import note_specgram
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
note_specgram('D:\PBL\music_3.wav', ax)
#list_1 = ['D:\PBL\music_2.wav']
#plot_notes(list_1)
plt.show()
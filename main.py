import cv2
import matplotlib.pyplot as plt
from PIL import Image
import rainbow_gramlist
import rainbow_gramself
import RPCA
import animation
import console

path = 'D:\PBL\music_3.wav'
console.discription()
begin = console.start()
console.mp3towav(path)
if begin == '1':
    rainbow_gramself.note_specgram(r'D:\PBL\Program\Record\music_sample\{}.wav'.format(path[7:-4]), showdata=True)
if begin == '2':
    list_1 = ['D:\PBL\C5-C6.wav','D:\PBL\C4-C5_p.wav']
    rainbow_gramlist.plot_notes(list_1)
if begin == '3':
    animation.animat('D:\PBL\Program\Record\music_sample\{}.wav'.format(path[7:-4]))
if begin == '4':
    pass
plt.show()
#RPCA.note_specgram('D:\PBL\music_2.wav')

raw_img1 = r'D:\PBL\Program\Record\result_map\single_sample\music_2.png'
raw_img2 = r'D:\PBL\Program\Record\result_map\single_sample\music.png'
hash_img1 = cv2.imread(raw_img1)
hash_img2 = cv2.imread(raw_img2)
cosine_img1 = Image.open(raw_img1)
cosine_img2 = Image.open(raw_img2)
console.similarily(hash_img1,hash_img2,cosine_img1,cosine_img2)
console.discription()
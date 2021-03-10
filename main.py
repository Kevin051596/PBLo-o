import time
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import rainbow_gramlist
import rainbow_gramself
import animation
import cosine
import hash

def recommend(cosin):
    if cosin>0.8 :
        print('真不錯')
    else :
        print('加油')

#animation_specgram('D:\PBL\C4.wav', ax , fig)
#list_1 = ['D:\PBL\C5-C6.wav','D:\PBL\C4-C5_p.wav']
#rainbow_gramlist.plot_notes(list_1)
rainbow_gramself.note_specgram('D:\PBL\C3-C4 piano.wav')
plt.show()

raw_img1 = r'D:\PBL\Program\Record\result_map\music_2.png'
raw_img2 = r'D:\PBL\Program\Record\result_map\music.png'
img1 = cv2.imread(raw_img1)
img2 = cv2.imread(raw_img2)

start=time.time()
ahash_str1=hash.aHash(img1)
ahash_str2=hash.aHash(img2)

phash_str1=hash.pHash(img1)
phash_str2=hash.pHash(img2)

dhash_str1=hash.dHash(img1)
dhash_str2=hash.dHash(img2)
a_score=1-hash.hammingDist(ahash_str1, ahash_str2)*1./(128*128/4)
p_score=1-hash.hammingDist(phash_str1, phash_str2)*1./(128*128/4)
d_score=1-hash.hammingDist(dhash_str1, dhash_str2)*1 /(128*128/4)

end=time.time()
print('a_score:{},p_score:{},d_score{}'.format(a_score,p_score,d_score))
print("Total Spend time：", str((end - start) / 60)[0:6] + "分钟")

image1 = Image.open(r'D:\PBL\Program\Record\result_map\music_2.png')
image2 = Image.open(r'D:\PBL\Program\Record\result_map\music.png')
cosin = cosine.image_similarity_vectors_via_numpy(image1, image2)
print('圖片餘弦相似度',cosin)

recommend(cosin)
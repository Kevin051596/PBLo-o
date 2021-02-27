import time
import cv2
import matplotlib.pyplot as plt
from PIL import Image
from rainbow_gram import note_specgram
from cosine import image_similarity_vectors_via_numpy
from hash import aHash
from hash import pHash
from hash import dHash
from hash import hammingDist

def recommend(cosin):
    if cosin>0.8 :
        print('真不錯')
    else :
        print('加油')


fig, ax = plt.subplots()
note_specgram('D:\PBL\C4.wav', ax)
#list_1 = ['D:\PBL\music_2.wav']
#plot_notes(list_1)
fig.savefig('plot2.png')

raw_img1 = r'D:\PBL\Program\Record\result_map\plot.png'
raw_img2 = r'D:\PBL\Program\Record\result_map\plot2.png'
img1 = cv2.imread(raw_img1)
img2 = cv2.imread(raw_img2)

start=time.time()
ahash_str1=aHash(img1)
ahash_str2=aHash(img2)

phash_str1=pHash(img1)
phash_str2=pHash(img2)

dhash_str1=dHash(img1)
dhash_str2=dHash(img2)
a_score=1-hammingDist(ahash_str1, ahash_str2)*1./(32*32/4)
p_score=1-hammingDist(phash_str1, phash_str2)*1./(32*32/4)
d_score=1-hammingDist(dhash_str1, dhash_str2)*1 /(32*32/4)

end=time.time()
print('a_score:{},p_score:{},d_score{}'.format(a_score,p_score,d_score))
print("Total Spend time：", str((end - start) / 60)[0:6] + "分钟")

image1 = Image.open(r'D:\PBL\Program\Record\result_map\plot.png')
image2 = Image.open(r'D:\PBL\Program\Record\result_map\plot2.png')
cosin = image_similarity_vectors_via_numpy(image1, image2)
print('圖片餘弦相似度',cosin)

recommend(cosin)
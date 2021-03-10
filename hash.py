import cv2
import time
import numpy as np


#均值哈希算法
def aHash(img):
    img=cv2.resize(img,(8,8))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    np_mean = np.mean(gray)                           # 求numpy.gray平均值
    ahash_01 = (gray>np_mean)+0                       # 大于平均值=1，否则=0
    ahash_list = ahash_01.reshape(1,-1)[0].tolist()   # 攤開並用列表顯示
    ahash_str = ''.join([str(x) for x in ahash_list])
    return ahash_str


def pHash(img):
    img = cv2.resize(img, (32, 32))    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dct = cv2.dct(np.float32(gray))
    dct_roi = dct[0:8, 0:8]            

    avreage = np.mean(dct_roi)
    phash_01 = (dct_roi>avreage)+0
    phash_list = phash_01.reshape(1,-1)[0].tolist()
    phash_str = ''.join([str(x) for x in phash_list])
    return phash_str

def dHash(img):
    img=cv2.resize(img,(9,8))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #每行前一个像素大于后一个像素为1，相反为0，生成哈希值
    hash_str0 = []
    for i in range(8):
        hash_str0.append(gray[:, i] > gray[:, i + 1])
    hash_str1 = np.array(hash_str0)+0
    hash_str2 = hash_str1.T
    hash_str3 = hash_str2.reshape(1,-1)[0].tolist()
    dhash_str = ''.join([str(x) for x in hash_str3])
    return dhash_str


def hammingDist(s1, s2):
    assert len(s1) == len(s2)
    return sum([ch1 != ch2 for ch1, ch2 in zip(s1, s2)])
    

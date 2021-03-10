from PIL import Image
from numpy import average, dot, linalg

#對圖片進行統一化處理
def get_thum(image, size=(64,64), greyscale=False):
    #利用image對影象大小重新設定, Image.ANTIALIAS為高質量的
    image = image.resize(size, Image.ANTIALIAS)
    if greyscale:
        #將圖片轉換為L模式，其為灰度圖，其每個畫素用8個bit表示
        image = image.convert('L')
    return image

#計算圖片的餘弦距離
def image_similarity_vectors_via_numpy(image1, image2):
    image1 = get_thum(image1)
    image2 = get_thum(image2)
    images = [image1, image2]
    vectors = []
    norms = []
    for image in images:
        vector = []
        for pixel_tuple in image.getdata():
            vector.append(average(pixel_tuple))
        vectors.append(vector)
        #linalg=linear（線性）+algebra（代數），norm則表示範數
        #求圖片的範數？？
        norms.append(linalg.norm(vector, 2))
    a, b = vectors
    a_norm, b_norm = norms
    #dot返回的是點積，對二維陣列（矩陣）進行計算
    res = dot(a / a_norm, b / b_norm)
    return res



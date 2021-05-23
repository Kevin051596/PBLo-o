"""
Various utilities for pretty console output
Ported nigh-verbatim from a similar file I use for node
"""
import os
import time as sysTime
import shutil
import picturesimilary
import pandas
from pydub import AudioSegment

class colors:
    END = "\033[0m"
    BRIGHT = "\033[1m"
    DIM = "\033[2m"
    UNDERSCORE = "\033[4m"
    BLINK = "\033[5m"

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    DK_RED = "\033[41m"
    DK_GREEN = "\033[42m"
    DK_YELLOW = "\033[43m"
    DK_BLUE = "\033[44m"
    DK_MAGENTA = "\033[45m"
    DK_CYAN = "\033[46m"
    DK_WHITE = "\033[47m"

timers = {}

def trans_mp3_to_wav(path, output):
    song = AudioSegment.from_file(path,format="mp3")
    song = song.set_frame_rate(44100)
    song = song.set_channels(2)
    song = song.set_sample_width(2)
    song.export(output + ".wav", format="wav")

def start():
    print(colors.YELLOW + "[選擇你要的功能]\n-單個音檔：1\n-多個音檔：2\n-動畫呈現：3\n-取消此動作：4" + colors.END)
    all = input("→ → → → → → → →")
    return all
def fmt(iterable):
    return " ".join(str(i) for i in iterable)
def h1(*args):
    print(colors.BRIGHT, fmt(args), colors.END)
def wait(*args):
    input(colors.BLUE + fmt(args) + colors.END)
def log(*args):
    print(colors.YELLOW, fmt(args), colors.END)
def info(*args):
    print(colors.DIM + "\t", fmt(args), colors.END)
def debug(*args):
    print(colors.DK_BLUE + "\t", fmt(args), colors.END)
def warn(*args):
    print(colors.DK_CYAN + "WARN:\t" + colors.END + colors.CYAN, fmt(args), colors.END)
def error(*args):
    print(colors.DK_RED + colors.BLINK + "ERROR:\t" + colors.END + colors.RED, fmt(args), colors.END)
def time(key):
    timers[key] = sysTime.time()
def timeEnd(key):
    if key in timers:
        t = sysTime.time() - timers[key]
        print("\t" + str(t) + colors.DIM  + " s \t" + key + colors.END)
        del timers[key]
def notify(*args):
    # Play bell
    print('\a')
    # Attempt to send a notification (will fail, but not crash, if not on macOS)
    os.system("""
          osascript -e 'display notification "{}" with title "{}"'
          """.format(args[0], fmt(args[1:])))

def mp3towav(path):
    mp3towav = r"{}.wav".format(path[11:-4])
    mp3towav_path =r"D:\204 PBL\Program\Record\music_sample\{}.wav".format(path[11:-4])
    try:
        os.remove(mp3towav_path)
        wav = trans_mp3_to_wav(path,'{}'.format(path[11:-4]))
        shutil.move(mp3towav, r"D:\204 PBL\Program\Record\music_sample")
    except OSError as error:
        wav = trans_mp3_to_wav(path,'{}'.format(path[11:-4]))
        shutil.move(mp3towav, r"D:\204 PBL\Program\Record\music_sample")
        print(colors.YELLOW + "Wav_file({}) is create successfully".format(mp3towav) + colors.END)
    else:
        print(colors.YELLOW + "Wav_file({}) is update successfully".format(mp3towav) + colors.END)

def newspectrum(path,fig):
    specturm = r"{}.png".format(path[39:-4])
    specturmpath = r"D:\204 PBL\Program\Record\result_map\single_sample\{}.png".format(path[39:-4])
    try:
        os.remove(specturmpath)
        fig.savefig(specturm,
                    bbox_inches='tight',
                    pad_inches=0,
                    format='png',
                    dpi= 300
                    )
        shutil.move(specturm,r"D:\204 PBL\Program\Record\result_map\single_sample")
    except OSError as error:
        fig.savefig(specturm,
                    bbox_inches='tight',
                    pad_inches=0,
                    format='png',
                    dpi =300
                    )
        shutil.move(specturm,r"D:\204 PBL\Program\Record\result_map\single_sample")
        print(colors.YELLOW + "File({}) is create successfully".format(specturm) + colors.END)
    else:
        print(colors.YELLOW + "File({}) is update successfully".format(specturm) + colors.END)

def xlsx(list,path):
    df = pandas.DataFrame(data=list)
    excel = r"{}.xlsx".format(path[39:-4])
    excel_path = r"D:\204 PBL\Program\Record\data\{}.xlsx".format(path[39:-4])
    try:
        os.remove(excel_path)
        df.to_excel(excel)
        shutil.move(excel, r"D:\204 PBL\Program\Record\data")
    except OSError as error:
        df.to_excel(excel)
        shutil.move(excel, r"D:\204 PBL\Program\Record\data")
        print(colors.YELLOW + "Excel_file({}) is create successfully".format(excel) + colors.END)
    else:
        print(colors.YELLOW + "Excel_file({}) is update successfully".format(excel) + colors.END)

def animation_output(path,ani):
    animation_path = r"D:\204 PBL\Program\Record\video\{}_animation.mp4".format(path[39:-4])
    animation = r"{}_animation.mp4".format(path[39:-4])
    try:
        os.remove(animation_path)
        ani.save(animation)
        shutil.move(animation, r"D:\204 PBL\Program\Record\video")
    except OSError as error:
        ani.save(animation)
        shutil.move(animation, r"D:\204 PBL\Program\Record\video")
        print(colors.YELLOW + "Animation({}) is create successfully".format(animation) + colors.END)
    else:
        print(colors.YELLOW + "Animation({}) is update successfully".format(animation) + colors.END)
def discription():
    print(colors.BRIGHT + "==================================================================" + colors.END)    
def similarily(hash_img1,hash_img2,cosine_img1,cosine_img2):
    start=sysTime.time()
    ahash_str1=picturesimilary.aHash(hash_img1)
    ahash_str2=picturesimilary.aHash(hash_img2)

    phash_str1=picturesimilary.pHash(hash_img1)
    phash_str2=picturesimilary.pHash(hash_img2)

    dhash_str1=picturesimilary.dHash(hash_img1)
    dhash_str2=picturesimilary.dHash(hash_img2)
    a_score=1-picturesimilary.hammingDist(ahash_str1, ahash_str2)*1./(32*32/4)
    p_score=1-picturesimilary.hammingDist(phash_str1, phash_str2)*1./(32*32/4)
    d_score=1-picturesimilary.hammingDist(dhash_str1, dhash_str2)*1 /(32*32/4)

    end=sysTime.time()
    print(colors.UNDERSCORE + 'a_score: {}, p_score: {}, d_score: {}'.format(a_score,p_score,d_score) + colors.END)
    print(colors.GREEN +"Total Spend time：", str((end - start) / 60)[0:6] + "分鐘" + colors.END)

    cosin = picturesimilary.image_similarity_vectors_via_numpy(cosine_img1, cosine_img2)
    print(colors.UNDERSCORE + '圖片餘弦相似度: {}'.format(cosin) + colors.END)

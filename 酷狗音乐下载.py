from 下载器 import *
from 歌单获取器 import *
from 歌词格式转换器 import *
import os

try: #检测音乐文件夹，没有则新建
    os.mkdir('音乐')
except:
    print('检测到音乐文件夹已存在')

mode = input('请填写下载模式(填纯数字)\n'
             '<1>下载整个歌单\n'
             '<2>根据歌曲名称下载单首歌曲\n'
             '<3>根据哈希值下载\n'
             '<4>导入文件(请先填写好"歌单哈希值列表.txt")\n'
             '<5>转换utf-8为gbk\n')

if mode == '1':
    get_song_list()
    if input("歌单获取完成，已保存在<歌单列表.txt>，是否一键下载？输入y确认") == 'y':
        download_list()
elif mode == '2':
    quality = input('请选择歌曲品质(填纯数字),可在酷狗音乐客户端进度条上面查看\n'
          '<1>标准(大部分允许下载)\n'
          '<2>高品(很少有允许下载)\n'
          '<3>超高品(不允许)\n'
          '<4>无损(不允许)\n')
    # quality = 1
    download_name(int(quality))
elif mode == '3':
    lyrics(download_hash(input('请输入哈希值')))
elif mode == '4':
    download_list()
elif mode == '5':
    utf8_to_gbk()

if input("是否打开文件夹？输入y确认") == 'y': #打开文件夹
    os.system("explorer 音乐\n")

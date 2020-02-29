import os
import easygui as eg

try:  # 检测音乐文件夹，没有则新建
    os.mkdir('音乐')
    os.mkdir('数据')
except:
    print('检测到音乐文件夹已存在')
with open('数据/cookies.txt','a'):
    pass
with open('数据/歌单列表.txt','a'):
    pass
with open('数据/歌单哈希值列表.txt','a'):
    pass
from 下载器 import *
from 歌单获取器 import *
from 歌词格式转换器 import *


def download():
    # 选择模式
    mode_list = ['下载整个歌单', '根据歌曲名称下载', '根据哈希值下载', '导入文件批量下载', '转换utf-8为gbk', '更新cookies']
    mode = eg.choicebox(msg='请选择下载模式', title='选择模式', choices=mode_list)

    if mode == '下载整个歌单':
        url = easygui.enterbox('请输入分享歌单的链接(支持酷狗码和QQ空间分享)', '输入连接')
        if (type(eval(url)) == int):
            kugou_code(url)
        else:
            get_song_list(url)

        if eg.ynbox(msg='歌单获取完成，已保存在<歌单列表.txt>，是否一键下载？', title='一键下载', choices=['是', '否']):
            download_list()
    elif mode == '根据歌曲名称下载':
        quality_list = ['标准(大部分允许下载)', '高品(很少有允许下载)', '超高品(不允许)', '无损(不允许)']
        quality = eg.choicebox(choices=quality_list, msg='选择音质')
        quality_dict = {}
        num = 1
        for i in quality_list:
            quality_dict[i] = num
            num += 1
        download_name(quality_dict[quality])
    elif mode == '根据哈希值下载':
        lyrics(download_hash(eg.enterbox('请输入哈希值'), True), eg.boolbox('是否下载歌词？', choices=['是', '否']))
    elif mode == '导入文件批量下载':
        download_list()
    elif mode == '转换utf-8为gbk':
        utf8_to_gbk()
    elif mode == '更新cookies':
        with open('数据/cookies.txt', 'r') as f:
            cookies_old = f.read()    
        cookies = eg.textbox('输入cookies,可在浏览器酷狗音乐页面按f12寻找\n下面的是原来的cookies,请删除后更改', '更新cookies', cookies_old)
        if cookies:
            with open('数据/cookies.txt', 'w') as f:
                f.write(cookies)
    else_mode = eg.choicebox(msg='本次操作已完成，是否进行其他操作', choices=['继续使用', '打开文件夹', '关闭程序'])
    if else_mode == '继续使用':#循环调用
        download()
    elif else_mode == '打开文件夹':
        os.system("explorer 音乐\n")

#调用函数
download()

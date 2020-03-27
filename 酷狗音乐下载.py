try:  # 检测音乐文件夹，没有则新建
    os.mkdir('音乐')
    os.mkdir('数据')
except:
    print('检测到音乐文件夹已存在')
with open('数据/cookies.txt', 'a'):
    pass
with open('数据/歌单列表.txt', 'a'):
    pass
with open('数据/歌单哈希值列表.txt', 'a'):
    pass

import time
from 下载组件 import *
import os
import easygui

song_download = kugou_download()


def download():
    # 选择模式
    mode_list = ['输入酷狗码', '根据歌曲名称下载', '根据哈希值下载',
                 '导入文件批量下载', '转换utf-8为gbk', '更新cookies']
    mode = easygui.choicebox(msg='请选择下载模式', title='选择模式', choices=mode_list)
    if mode == '输入酷狗码':
        code = easygui.enterbox('请输入酷狗码', '输入酷狗码')
        code_return = kugou_code(code)
        print(type(code_return))
        if str(type(code_return)) == "<class 'list'>":
            # 写入数据
            with open("数据/歌单列表.txt", "w", encoding="utf-8") as f:
                with open("数据/歌单哈希值列表.txt", "w") as d:
                    for i in code_return:
                        song_name = i['filename']
                        song_hash = i['hash']
                        f.write(song_name + '\n')
                        d.write(song_hash + '\n')
                    code_list_mode = easygui.choicebox(msg='歌单列表获取完成\n是否继续其他操作？', choices=['打开歌单列表txt', '一键下载全部', '关闭'])
                    if code_list_mode == '打开歌单列表':
                        os.system("数据/歌单列表.txt")
                    elif code_list_mode == '一键下载全部':
                        lyrics_mode = easygui.boolbox(msg='是否需要一键下载全部歌词？', choices=['是', '否'])
                        for i in code_return:
                            print(song_download.download_main(i['hash'], lyrics_mode))
                            time.sleep(1)
        else:
            lyrics_mode = easygui.boolbox('是否下载歌词？', choices=['是', '否'])
            easygui.msgbox(msg=song_download.download_main(code_return, lyrics_mode), ok_button='继续')


    elif mode == '根据歌曲名称下载':
        song_name = easygui.enterbox(msg='请输入歌曲名称')
        song_name_json = song_download.download_name(song_name)
        i = 1
        song_list = []
        for song in song_name_json['data']['lists']:
            file_name = str(i) + ' ' + song['FileName'].replace('<em>', '').replace('</em>', '').replace('<\\\\/em>',
                                                                                                         '')
            song_list.append(file_name)
            i += 1
        num = int(easygui.choicebox(msg='请在以上结果中选择你要下载的歌曲', choices=song_list).split(" ")[0])
        lyrics_mode = easygui.boolbox('是否下载歌词？', choices=['是', '否'])
        easygui.msgbox(
            msg=song_download.download_main(song_name_json['data']['lists'][num - 1]['FileHash'], lyrics_mode),
            ok_button='继续')

    elif mode == '导入文件批量下载':
        with open('数据/歌单哈希值列表.txt', 'r') as f:
            song_hash_list = f.read().split()
        lyrics_mode = easygui.boolbox(msg='是否需要一键下载全部歌词？', choices=['是', '否'])
        for i in song_hash_list:
            print(song_download.download_main(i, lyrics_mode))
            time.sleep(1)

    elif mode == '更新cookies':
        with open('数据/cookies.txt', 'r') as f:
            cookies_old = f.read()
        cookies = easygui.textbox(
            '输入cookies,可在浏览器酷狗音乐页面按f12寻找\n下面的是原来的cookies,请删除后更改', '更新cookies', cookies_old)
        if cookies:
            with open('数据/cookies.txt', 'w') as f:
                f.write(cookies)
    else_mode = easygui.choicebox(msg='本次操作已完成，是否进行其他操作', choices=[
        '继续使用', '打开文件夹', '关闭程序'])
    if else_mode == '继续使用':  # 循环调用
        download()
    elif else_mode == '打开文件夹':
        os.system("explorer 音乐\n")


# 调用函数
download()

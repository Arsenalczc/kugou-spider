import json
from urllib import parse
import requests
import time
import easygui as eg

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4023.0 Safari/537.36 Edg/81.0.396.0'}
with open('数据/cookies.txt', 'r') as f:
    cookies = f.read()


# cookies='kg_mid=9526c011844091cafd12889f2c7e6ae6; _WCMID=164540295d9227c4c1934f5a; kg_dfid=10C0M20bBwoB0ROC2j3kckWa; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1579179321,1580200379,1580210126; kg_mid_temp=9526c011844091cafd12889f2c7e6ae6; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1580212346'

def str_to_dict(cookies):
    cookies_dict = {}
    cookies1 = cookies.replace(' ', '')
    cookies_list = cookies1.split(';')
    for str1 in cookies_list:
        key, values = str1.split('=', 1)
        cookies_dict[key] = values
    return cookies_dict


def download_hash(song_hash, is_GUI):
    url_json2 = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery191044011229047114075_1566198263706&hash={}'.format(
        song_hash)
    page2 = requests.get(url=url_json2, headers=headers, cookies=str_to_dict(cookies)).text
    song_json2 = json.loads(page2[42:-2])
    with open('数据/log.txt', 'w', encoding='utf-8') as log:
        log.write(str(song_json2))
    if song_json2['status'] == 0:
        print('cookies过期或发生其他错误，请重试')
        print('程序将退出')
        quit(1)
    # 傻逼文件名的检测替换
    file_name_error = ['"', '?', '/', '*', ':', '\\', '|', '<', '>']
    for file_name in file_name_error:
        if song_json2['data']['audio_name'].find(file_name) != -1:
            song_json2['data']['audio_name'] = song_json2['data']['audio_name'].replace(file_name, ' ')
    song_url = song_json2['data']['play_url']
    song_name = song_json2['data']['audio_name']
    song_length = int(song_json2['data']['timelength'])
    song_free = song_json2['data']['is_free_part']  # 试听歌曲为1，普通歌曲为0
    if song_url == '' and is_GUI:  # 检测歌曲是否能下载
        eg.msgbox(msg='❌歌曲<{}>无数据或需要付费下载'.format(song_name), title='错误', ok_button='好的')
    else:
        try:  # 检测是否存在已下载文件
            notice_file_name = ''
            notice = ''
            if song_free == 1:  # 试听歌曲检测
                notice = '⚠歌曲为试听版，请核实'
                notice_file_name = '[试听]'
            with open('音乐/' + notice_file_name + song_name + '.mp3', 'xb') as f:
                song = requests.get(url=song_url, headers=headers, cookies=str_to_dict(cookies))
                f.write(song.content)
            song_length_format = str(int(song_length / 1000) // 60) + ":" + str(int(song_length / 1000) % 60)

            if is_GUI:
                eg.msgbox(msg='✔歌曲<{}>下载完成\n歌曲时长{}\n'.format(song_name, song_length_format) + notice, title='成功',
                          ok_button='继续')
            else:
                print('✔歌曲<{}>下载完成\n歌曲时长{}\n'.format(song_name, song_length_format) + notice)
        except:
            if is_GUI:
                eg.msgbox(msg='⚠歌曲<' + song_name + '>已存在', ok_button='继续')
            else:
                print('⚠歌曲<' + song_name + '>已存在')
        return song_json2


def download_name(mode):
    name = eg.enterbox(msg='输入歌曲名称')
    url_name = parse.quote(name)
    url_name = url_name.replace('%20', '+')
    url_json1 = 'https://songsearch.kugou.com/song_search_v2?callback=jQuery11240770641348037286_1566198223730' \
                '&keyword={}&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection' \
                '=1&privilege_filter=0&_=1566198223734'.format(url_name)
    page1 = requests.get(url=url_json1, headers=headers).text
    song_json = json.loads(page1[41:-2])
    i = 0
    song_list = []
    song_dict = {}
    for song in song_json['data']['lists']:
        file_name = song['FileName'].replace('<em>', '').replace('</em>', '')
        song_dict[file_name] = i
        song_list.append(file_name)
        i += 1
    i = int(song_dict[eg.choicebox(msg='请在以上结果中选择你要下载的歌曲', choices=song_list)])
    # i=int(input('请在以上结果中选择你要下载的歌曲(填数字编号)\n'))-1
    lyrics_mode = eg.boolbox('是否下载歌词？', choices=['是', '否'])
    if mode == 1:  # 流畅
        lyrics(download_hash(song_json['data']['lists'][i]['FileHash'], True), lyrics_mode)
    elif mode == 2:  # 高品
        lyrics(download_hash(song_json['data']['lists'][i]['HQFileHash'], True), lyrics_mode)
    elif mode == 3:  # 超高
        lyrics(download_hash(song_json['data']['lists'][i]['SQFileHash'], True), lyrics_mode)
    elif mode == 4:  # 无损
        lyrics(download_hash(song_json['data']['lists'][i]['ResFileHash'], True), lyrics_mode)


def download_list():
    with open('数据/歌单哈希值列表.txt', 'r') as f:
        song_hash_list = f.read().split()
    lyrics_mode = eg.boolbox(msg='是否需要一键下载全部歌词？', choices=['是', '否'])
    for i in song_hash_list:
        lyrics(download_hash(i, False), lyrics_mode)
        time.sleep(1)


def lyrics(json_list, mode):
    # print(type(json_list['data']['lyrics']))
    if str(json_list).find('纯音乐，请欣赏') != -1:
        print('✔已检测到纯音乐，不需要歌词')
    elif json_list == None or json_list['data']['lyrics'] == '':
        print('❌此歌曲无歌词')
    else:
        if mode:
            with open('音乐/' + json_list['data']['audio_name'] + '.lrc', 'w', encoding='gb18030') as f:
                f.write(json_list['data']['lyrics'].replace('\n', '').replace('\ufeff', '').replace('[id:$00000000]',
                                                                                                    '').replace('\r',
                                                                                                                '', 1))
            print('歌词下载完成\n')

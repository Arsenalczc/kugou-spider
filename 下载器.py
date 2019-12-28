import json
from urllib import parse
import requests
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3872.0 Safari/537.36 Edg/78.0.244.0'}
cookies = 'kg_mid=2ccec311dd30b13705a140e6b7710e64; kg_dfid=1afQI30nxtgd0PXOun1bVc82; KuGoo=KugooID=399348742&KugooPwd=8C0B5256FAF5DA6FA18C286748812312&NickName=%u98a2%u5929&Pic=http://imge.kugou.com/kugouicon/165/20190125/20190125113410491671.jpg&RegState=1&RegFrom=&t=f88505dc15198cc5461f00828f32ba674e83f14f443c6c90881f827fe07494ff&a_id=1014&ct=1566202440&UserName=%u006b%u0067%u006f%u0070%u0065%u006e%u0033%u0039%u0039%u0033%u0034%u0038%u0037%u0034%u0032; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1566196509,1566215357,1566657663,1567046009; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1567046188'


def str_to_dict(cookies):
    cookies_dict = {}
    cookies1 = cookies.replace(' ', '')
    cookies_list = cookies1.split(';')
    for str1 in cookies_list:
        key, values = str1.split('=', 1)
        cookies_dict[key] = values
    return cookies_dict


def download_hash(song_hash):
    url_json2 = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery191044011229047114075_1566198263706&hash={}&album_id=1966068&dfid=1afQI30nxtgd0PXOun1bVc82&mid=2ccec311dd30b13705a140e6b7710e64&platid=4&_=1566198263708'.format(
        song_hash)
    page2 = requests.get(url=url_json2, headers=headers, cookies=str_to_dict(cookies)).text
    song_json2 = json.loads(page2[42:-2])
    song_url = song_json2['data']['play_url']
    song_name = song_json2['data']['audio_name']
    song_length = int(song_json2['data']['timelength'])
    song_free = song_json2['data']['is_free_part'] #试听歌曲为1，普通歌曲为0
    with open('log.txt', 'w', encoding='utf-8') as log:
        log.write(str(song_json2))
    if song_url == '': #检测歌曲是否能下载
        print('❌歌曲<{}>无数据或需要付费下载'.format(song_name))
    else:
        try:  # 检测是否存在已下载文件
            with open('音乐/' + song_name + '.mp3', 'xb') as f:
                song = requests.get(url=song_url, headers=headers)
                f.write(song.content)
            print('✔歌曲<{}>下载完成'.format(song_name))
            print("歌曲时长"+str(int(song_length/1000)//60)+":"+str(int(song_length/1000)%60))
            if song_free==1: #试听歌曲检测
                print('⚠歌曲可能为试听版，请核实')
        except:
            print('⚠歌曲<' + song_name + '>已存在')
        return song_json2


def download_name(mode):
    name = input('输入歌曲名称\n')
    print('单曲获取较慢，请耐心等待')

    url_name = parse.quote(name)
    url_name = url_name.replace('%20', '+')
    url_json1 = 'https://songsearch.kugou.com/song_search_v2?callback=jQuery11240770641348037286_1566198223730' \
                '&keyword={}&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection' \
                '=1&privilege_filter=0&_=1566198223734'.format(url_name)
    page1 = requests.get(url=url_json1, headers=headers).text
    song_json = json.loads(page1[41:-2])
    i = 1
    for song in song_json['data']['lists']:
        file_name = str(i)+'. '+song['FileName']
        print(file_name.replace('<em>','').replace('</em>',''))
        i+=1
    i=int(input('请在以上结果中选择你要下载的歌曲(填数字编号)\n'))-1
    if mode == 1:  # 流畅
        lyrics(download_hash(song_json['data']['lists'][i]['FileHash']))
    elif mode == 2:  # 高品
        lyrics(download_hash(song_json['data']['lists'][i]['HQFileHash']))
    elif mode == 3:  # 超高
        lyrics(download_hash(song_json['data']['lists'][i]['SQFileHash']))
    elif mode == 4:  # 无损
        lyrics(download_hash(song_json['data']['lists'][i]['ResFileHash']))


def download_list():
    with open('歌单哈希值列表.txt', 'r') as f:
        song_hash_list = f.read().split()
    lyrics_mode = input('是否需要一键下载全部歌词？需要请输入<y>')
    for i in song_hash_list:
        lyrics(download_hash(i), lyrics_mode)
        time.sleep(0.2)
    print('歌曲已经全部下载完成，感谢使用')


def lyrics(json_list, *mode):
    # print(type(json_list['data']['lyrics']))
    if str(json_list).find('纯音乐，请欣赏') != -1:
        print('✔已检测到纯音乐，不需要歌词')
    elif json_list == None or json_list['data']['lyrics'] == '':
        print('❌此歌曲无歌词')
    else:
        if mode != 'y' or 'n':
            mode = input('是否需要下载歌词？需要请输入<y>')
        if mode == 'y':
            with open('音乐/' + json_list['data']['audio_name'] + '.lrc', 'w', encoding='gb18030') as f:
                f.write(json_list['data']['lyrics'].replace('\n', '').replace('\ufeff', '').replace('[id:$00000000]','').replace('\r','', 1))
            print('歌词下载完成')

import  easygui
from lxml import etree
import requests
from ast import literal_eval

def get_song_list():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3872.0 Safari/537.36 Edg/78.0.244.0'}
    url = easygui.enterbox('请输入分享歌单的链接','输入连接')
    page = requests.get(url=url, headers=headers).text
    html = etree.HTML(page)


    end = html.xpath('//script[2]')[0].text.find('],//当前页面歌曲信息')
    print(end)
    song_list = literal_eval(html.xpath('//script[2]')[0].text[31:end])
    with open("数据/歌单列表.txt", "w",encoding="utf-8") as f:
        with open("数据/歌单哈希值列表.txt", "w") as d:
            print('歌单列表获取完成\n👇以下是列表中的歌曲👇')
            for i in song_list:
                song_name = i['audio_name']
                song_hash = i['hash']
                f.write(song_name + '\n')
                d.write(song_hash + '\n')
                print(song_name)


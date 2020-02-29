import  easygui
from lxml import etree
import requests
from ast import literal_eval

def get_song_list(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3872.0 Safari/537.36 Edg/78.0.244.0'}
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

def kugou_code(code):
    data2 = {"appid": 1001, "clientver": 8392, "mid": "b1422385bca909d7ac9aadb285f05541",
            "clienttime": 636307277, "key": "1bb5ba48267c0a4750ecda8d7b10368c"}
    data = '{"appid":1001,"clientver":8392,"mid":"b1422385bca909d7ac9aadb285f05541","clienttime":636307277,"key":"1bb5ba48267c0a4750ecda8d7b10368c","data":"'+code+'"}'
    headers = {
        'User-Agent': 'Android800-AndroidPhone-10042-46-0-JsonRespHttpTransor-wifi'}
    cookies = 'cookie: kg_mid=b434c13fcd475da311e141a0cf532557; KuGooRandom=66451582539942780; kg_mid_temp=b434c13fcd475da311e141a0cf532557'

    page = requests.post(url="http://t.kugou.com/command/",data=data, headers=headers).text
    page = eval(page)

    json2 = data2
    json2["data"] = page["data"]['info']

    del json2['data']['name'], json2['data']['username'], json2['data']['img'], json2['data']['img_size']
    json2['data']['page'] = 1
    json2['data']['pagesize'] = json2['data']['count']
    del json2['data']['count']
    json2['data']['type'] = 3
    # json2 = '{"appid":1001,"clientver":8392,"mid":"b1422385bca909d7ac9aadb285f05541","clienttime":636307277,"key":"1bb5ba48267c0a4750ecda8d7b10368c","data":{"id":8,"type":3,"userid":"399348742","collect_type":0,"page":1,"pagesize":81}}'
    json2 = str(json2).replace("\'", "\"")

    json3 = requests.post(url='http://www2.kugou.kugou.com/apps/kucodeAndShare/app/', data=json2).text
    json3=eval(json3)
    song_list = json3['data']
    with open("数据/歌单列表.txt", "w",encoding="utf-8") as f:
        with open("数据/歌单哈希值列表.txt", "w") as d:
            print('歌单列表获取完成\n👇以下是列表中的歌曲👇')
            for i in song_list:
                song_name = i['filename']
                song_hash = i['hash']
                f.write(song_name + '\n')
                d.write(song_hash + '\n')
                print(song_name)
def utf8_to_gbk():
    file_name = input('请输入lrc歌词文件名').replace('"','')
    with open(file_name,'r',encoding='utf-8') as f:
        content = f.read()
        print(content)

    with open(file_name,'w',encoding='gb18030') as f:
        f.write(content.replace('\ufeff', ''))


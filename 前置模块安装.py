import os
print("检测前置中")
try:
    import json
except:
    print("缺少前置，正在补全")
    os.system("pip install json")
try:
    import lxml
except:
    print("缺少前置，正在补全")
    os.system("pip install lxml")
try:
    import requests
except:
    print("缺少前置，正在补全")
    os.system("pip install requests")
try:
    import urllib
except:
    print("缺少前置，正在补全")
    os.system("pip install urllib")
print("前置检测完成")

import urllib.request, sys, base64, json, os, time, baiduSearch, screenshot, re
from PIL import Image
from common import config
import pytesseract

# 配置appcode
config = config.open_accordant_config()

start = time.time()
# 开始截图
screenshot.check_screenshot()
screenshot.pull_screenshot()
host = 'http://text.aliapi.hanvon.com'
path = '/rt/ws/v1/ocr/text/recg'
method = 'POST'
appcode = config['appcode']  # 汉王识别appcode（填你自己的）
querys = 'code=74e51a88-41ec-413e-b162-bd031fe0407e'
bodys = {}
url = host + path + '?' + querys

im = Image.open(r"./screenshot.png")

img_size = im.size
w = im.size[0]
h = im.size[1]
print("xx:{}".format(img_size))

region = im.crop((70, 300, w - 70, 600))  # 裁剪的区域 百万超人 手机1080*1920 高度范围300~600
region.save("./crop_test1.png")

im = Image.open(r"./crop_test1.png")
text = pytesseract.image_to_string(im, lang='chi_sim')
print(text, end='\n\n')

keyword = ''.join(text)  # 识别的问题文本
keyword = re.sub(r"\d+.", "", keyword, 1)
convey = 'n'

if convey == 'y' or convey == 'Y':
    results = baiduSearch.search(keyword, convey=True)
elif convey == 'n' or convey == 'N' or not convey:
    results = baiduSearch.search(keyword)
else:
    print('输入错误')
    exit(0)
count = 0
for result in results:
    # print('{0} {1} {2} {3} {4}'.format(result.index, result.title, result.abstract, result.show_url, result.url))  # 此处应有格式化输出
    print('{0}'.format(result.abstract), end='\n\n')  # 此处应有格式化输出
    count = count + 1
    if (count == 2):
        break

end = time.time()
print('', end='\n\n')
print('程序用时：' + str(end - start) + '秒')
print(keyword)

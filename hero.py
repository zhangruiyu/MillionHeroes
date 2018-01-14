import urllib.request, sys, base64, json, os, time, baiduSearch, screenshot, re
from PIL import Image
import asyncio
import threading
from common import config
import pytesseract
import re

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

screenshot = Image.open(r"./screenshot.png")

img_size = screenshot.size
w = screenshot.size[0]
h = screenshot.size[1]
print("xx:{}".format(img_size))

arrayAnswer = []


def getAnswer():
    global arrayAnswer
    print("执行获取答案")
    # 获取答案
    regionAnswer = Image.open(r"./screenshot.png").crop((70, 600, w - 70, 1280))  # 裁剪的区域 百万超人 手机1080*1920 高度范围300~600
    # for i in range(1,1600):
    #     for j in range(1,1600):
    #         r, g, b,d = region.getpixel((i, j))
    #         print(region.getpixel((i, j)))
    #         if r == 138 & g == 148 & b == 156:
    #             b = 255
    #             g = 255
    #             r = 255
    #
    #         region.putpixel((i, j), (r, g, b))

    regionAnswer.save("./crop_test2.png")
    imAnswer = Image.open(r"./crop_test2.png")
    resultAnswer = pytesseract.image_to_string(imAnswer, lang='chi_sim')
    arrayAnswer = resultAnswer.split('\n')
    print("答案包含:::    " + resultAnswer.replace("\n", ','), end='\n\n')


def getBaiduData():
    global arrayAnswer
    print("执行获取问题")
    # 获取题目
    region = Image.open(r"./screenshot.png").crop((70, 300, w - 70, 600))  # 裁剪的区域 百万超人 手机1080*1920 高度范围300~600

    # 保存im
    region.save("./crop_test1.png")
    #
    im = Image.open(r"./crop_test1.png")
    text = pytesseract.image_to_string(im, lang='chi_sim').replace("\n", "")

    print("问题是:::::    " + text)

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
    print('', end='\n\n')

    for result in results:
        abstract  = result.abstract
        # print('{0} {1} {2} {3} {4}'.format(result.index, result.title, result.abstract, result.show_url, result.url))  # 此处应有格式化输出
        print('{0}'.format(abstract), end='\n\n')  # 此处应有格式化输出
        flag = ""

        for answer in arrayAnswer:
            if abstract.find(answer) > 0:
                flag = answer
                print("答案1选============     " + answer, end='\n\n')

        # print("答案1选============     " + answer, end='\n\n')
        #
        # if flag == "":
        #     flag.strip()
        #     for answer in [an for an in arrayAnswer if an.strip() != '']:
        #         na = '.*'.join([i for i in answer]) + '.*'
        #         print('na is ', na, 'abstract is ', abstract)
        #         if re.search(na, abstract):
        #             print("答案2选============        " + answer, end='\n\n')
        count = count + 1
        if (count == 2):
            break


t2 = threading.Thread(target=getAnswer)
t2.start()

t1 = threading.Thread(target=getBaiduData)
t1.start()
t1.join()
t2.join()
print('解析图片用时：' + str(time.time() - start) + '秒')

end = time.time()
print('', end='\n\n')
print('程序用时：' + str(end - start) + '秒')

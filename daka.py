#!/usr/bin/python3
# @File: daka.py
# --coding: utf-8--
# @Author: 孟德昊
# @Time: 2021年 09月 30日 20:57
# 说明:自动每日健康打卡
import time
import tkinter as tk
import tkinter.messagebox
import requests
from PIL import Image
from hashlib import md5
from selenium import webdriver
from lxml import etree
from time import sleep
# 实现规避检测
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
# 实现无可视化界面
from selenium.webdriver.edge.options import Options
#

class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()



#
if __name__ == "__main__":
    #风险规避
    option = EdgeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 无可视化操作
    caps = {
        "browserName": "MicrosoftEdge",
        "version": "",
        "platform": "WINDOWS",
        # 关键是下面这个
        "ms:edgeOptions": {
            'extensions': [],
            'args': [
                '--headless',
                '--disable-gpu'
            ]}
    }
    #UA伪装
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52'
    # }
    #网页页面获取
    # bro = webdriver.Edge(executable_path='./msedgedriver.exe', capabilities=caps)
    # bro = Edge(executable_path='./msedgedriver', capabilities=EDGE,options=option)
    bro = Edge(executable_path='E:\\python_lesson\\爬虫\\msedgedriver.exe',options=option)
    bro.get('https://pass.ujs.edu.cn/cas/login?service=http%3A%2F%2Fyun.ujs.edu.cn%2Fxxhgl%2Fyqsb%2Findex')
    #页面最大化
    bro.maximize_window()
    #获取页面内验证码图片 但是获取时会进行刷新图片 所以不可取
    # page_text = bro.page_source
    # tree = etree.HTML(page_text)
    # yanzheng_img_url ='https://pass.ujs.edu.cn/cas/'+tree.xpath('//*[@id="captchaImg"]/@src')[0]
    # yanzheng_img = requests.get(url=yanzheng_img_url,headers=headers).content
    # img_path = '验证码.jpg'
    # with open(img_path,'wb') as fp:
    #     fp.write(yanzheng_img)
    #将当前页面进行截图(可行)
    bro.save_screenshot('aa.png')
    #裁剪验证码区域图片（坐标）
    code_img_ele = bro.find_element_by_xpath('//*[@id="captchaImg"]')
    #获取标签坐标
    location = code_img_ele.location
    size = code_img_ele.size
    #裁剪不符合时，重新定坐标
    location['x'] = 1310
    location['y'] = 408
    size['width'] = 120
    size['height'] = 48
    print('location', location)
    print('size',size)
    rangle = (
    location['x'],location['y'],location['x']+size['width'],location['y']+size['height']
    )
    i = Image.open('./aa.png')
    code_img_name = '验证码.png'
    frame = i.crop(rangle)
    frame.save(code_img_name)

    #输入账号密码
    username = bro.find_element_by_id('username')
    password = bro.find_element_by_id('password')

    username.send_keys('xxxxxx')        #输入学号
    password.send_keys('xxxxxx')       #输入门户密码

    chaojiying = Chaojiying_Client('xxxxx', 'xxxxxxx', 'xxxxx')	#用户中心>>软件ID 生成一个替换 96001
    im = open('验证码.png', 'rb').read()													#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    yanzhengma = chaojiying.PostPic(im, 1902)
    # print(chaojiying.PostPic(im, 1902))												#1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
    #验证码输入
    yanzhengma_word = bro.find_element_by_id('captchaResponse')
    yanzhengma_word.send_keys(yanzhengma['pic_str'])
    print("输入成功")

    #确认登陆
    btn_login = bro.find_element_by_class_name('auth_login_btn')
    btn_login.click()

    # time.sleep(50)
    # bro.get(bro.current_url)
    # login_in(bro)
    time.sleep(10)
    #点击确认
    bro.find_element_by_class_name('weui_btn').click()

    bro.find_element_by_class_name('weui_btn').click()

    print('点击成功')
    # # print(btn_insert)
    # btn_insert.click()
    # print(bro.current_url)


    # time.sleep(30)
    # bro.get(bro.current_url)
    time.sleep(5)
    #输入体温
    yesterday =bro.find_element_by_id('xwwd')
    yesterday.send_keys('36')
    today = bro.find_element_by_id('swwd')
    today.send_keys('36')
    #选择无异常
    bro.find_element_by_xpath('//*[@id="qtyc"]/option[2]').click()
    # time.sleep(10)
    btn_submit = bro.find_element_by_id('button1')
    btn_submit.click()
    #关闭页面
    bro.quit()
    # print("打卡成功")
    #窗口提示打卡成功
    root = tk.Tk()
    root.withdraw()
    tkinter.messagebox.showinfo(title='提示', message='打卡成功')

import pyautogui
import webbrowser as web
from time import sleep
import os

# 获取当前屏幕分辨率
screenWidth, screenHeight = pyautogui.size()
# 03405197
currentMouseX, currentMouseY = pyautogui.position()
# pyautogui.FAILSAF123456aB-E = True
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01


# confidence = 0.9: 像素匹配度


class Robot():
    def __init__(self):
        pass

    # 用IE浏览器打开指定网址
    def ie_open_url(self, url):
        browser_path = r'C:\Program Files (x86)\Internet Explorer\iexplore.exe'
        web.register('IE', None, web.BackgroundBrowser(browser_path))
        web.get('IE').open_new_tab(url)
        print('use_IE_open_url  open url ending ....')

    # 打开exe
    def open_exe(self, path):
        os.startfile(path)

    # 浏览器最大化
    def ie_max(self, path):
        try:
            self.img_click(path)
        except:
            print('已经最大化')

    # 关闭exe
    def close_exe(self, exe_name):
        """
        :param exe_name: os.system("taskkill /F /IM iexplore.exe")
        :return:
        """
        os.system("taskkill /F /IM {}".format(exe_name))

    # 关闭浏览器
    def ie_close_url(self, path):
        try:
            # self.img_click('D:/img_rb/关闭浏览器.png')
            self.img_click(path)
            print('浏览器关闭成功')
        except:
            print('浏览器关闭失败')

    # 最大化
    def ie_big(self, path):
        try:
            # self.img_click('D:/img_rb/最大化浏览器.png')
            self.img_click(path)
        except:
            print('最大化浏览器失败')

    # ###############################################

    # 输入文字
    def type_text(self, text):
        pyautogui.typewrite(text)

    # 根据截图点击
    def img_click(self, img_path, num=1):
        # #在当前屏幕中查找指定图片(图片需要由系统截图功能截取的图)
        coords = pyautogui.locateOnScreen(img_path)
        # confidence = 0.9: 像素匹配度

        # #获取定位到的图中间点坐标
        x, y = pyautogui.center(coords)
        pyautogui.click(x=x, y=y, clicks=num, interval=0.0, button='left', duration=0.0, tween=pyautogui.linear)

    # 创建文件夹
    def crate_dir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            print('此文件夹已经存在')

    # 检测图片是否存在
    def img_check(self, img_path, t_all=100, t1=0.01):
        num = 0
        while num <= t_all:
            num += 1
            print(num)
            sleep(t1)
            try:
                # #在当前屏幕中查找指定图片(图片需要由系统截图功能截取的图)
                coords = pyautogui.locateOnScreen(img_path)
                print(coords)
                if coords:
                    break
                else:
                    continue

            except:
                print('图片检测失败')
                return False


    # 向下移动滑块
    def move_down(self, path, x=0, y=0):
        self.img_click(path)
        sleep(2)
        pyautogui.dragRel(x, y)
        sleep(2)

    # 重命名文件夹
    def re_name(self, data_name, new_name):
        """
        :param data_name: data_name = "CP_费用报销明细表_" + day + month + year + ".xls"
        :param new_name: new_name = "666666666666666666666666666666666666666.xls"
        :return: True
        """
        import os
        import datetime
        new_time = datetime.datetime.now()
        year = str(new_time).split('-')[0][2:4]
        month = str(new_time).split('-')[1]
        day = str(new_time).split('-')[2][:2]
        data_name_new = data_name + day + month + year + ".xls"
        try:
            os.remove(f'C:/Users/Administrator/Desktop/{new_name}')
        except:
            print('不存在')
        os.rename(f'C:/Users/Administrator/Desktop/{data_name_new}', f'C:/Users/Administrator/Desktop/{new_name}')

    # 鼠标滑块移动
    def rolling(self):
        pyautogui.scroll(100, x=100, y=100)

    # 截图
    def screen(self, x1, y1, x2, y2, path):
        """
        :param x1: 左侧，
        :param y1: 顶部，
        :param x2: 宽度
        :param y2: 高度
        :param path: 保存路径
        :return:
        """
        im = pyautogui.screenshot(region=(0, 0, 300, 400))
        im.save(path)

    # 验证码识别
    def img_dis(self, path):
        import pytesseract
        from PIL import Image

        image = Image.open(path)

        code = pytesseract.image_to_string(image)
        print(code)

    # 键盘操作
    def jianpan(self):
        pyautogui.press('esc')
        # 按住shift键
        pyautogui.keyDown('shift')
        # 放开shift键
        pyautogui.keyUp('shift')
        # 模拟组合热键
        pyautogui.hotkey('ctrl', 'c')

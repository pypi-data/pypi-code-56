from selenium import webdriver 
from time import sleep
import os

class whats_app_bot:
    def __init__(self) :
        path = os.path.dirname(os.path.realpath(__file__))
        path += "/chromedriver"
        try :
            self.driver = webdriver.Chrome(executable_path=path)
            self.driver.get('https://web.whatsapp.com/')
        except :
            print('Error : Chrome Driver path error')
            quit()
        input('Scan the QR code and Press any button to continue :) ')
        sleep(2)

    def send_text_to(self, title, msg, repeat = 1):
        self.title = title
        self.msg = msg 
        self.repeat = repeat # for sending same text multiple times

        # select the user
        try:
            user = self.driver.find_element_by_xpath("//span[@title = '{}']".format(self.title))
            user.click()
        except : 
            print('Error : Cannot Find User!')
        # select the message box 
        message_box = self.driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')

        for _ in range(self.repeat):
            message_box[0].send_keys(self.msg)
            send = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]')
            send.click()


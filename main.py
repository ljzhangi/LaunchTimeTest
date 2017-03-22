# -*- coding:UTF-8 -*-
import os
import string
import commands
from appium import webdriver
import datetime
import csv
import codecs

__author__ = 'Leo, Zhang'

# 返回文件的绝对地址
PATH = lambda p:os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class LaunchTime(object):

    # 测试需要用的环境变量
    PLATFORM_NAME = 'Android'
    PLATFORM_VERSION = string.strip(commands.getoutput('adb shell getprop ro.build.version.release'))  # 获取手机系统版本
    DEVICE_NAME = string.strip(commands.getoutput('adb shell getprop ro.serialno'))  # 获取手机SN号
    PHONE_NAME = string.strip(commands.getoutput('adb shell getprop ro.build.id'))

    def __init__(self, app, appPackage, appActivity):
        '''
        :param app: test app localed path
        :param appPackage: test app package
        :param appActivity: test app main activity
        '''
        print '##########Begin#################'
        # 建立字典,储存测试设备的信息
        desired_caps = {}
        desired_caps['platformName'] = self.PLATFORM_NAME
        desired_caps['platformVersion'] = self.PLATFORM_VERSION
        desired_caps['deviceName'] = self.DEVICE_NAME
        desired_caps['app'] = app
        desired_caps['appPackage'] = appPackage
        desired_caps['appActivity'] = appActivity
        desired_caps['noReset'] = True
        desired_caps['unicodeKeyboard'] = True
        desired_caps['resetKeyboard'] = True

        # 设置服务端驱动器
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        driver.implicitly_wait(60)
        self.driver = driver
        self.appActivity = appActivity

    def clear_env(self):
        print '##########End###################'
        os.system('adb shell am force-stop %s' % self.appActivity)
        self.driver.quit()

    def test_app_start(self):
        begin_time = self.get_current_time()
        print 'Start app: %s' % begin_time  # 输出app启动时的时间

        element = self.driver.find_element_by_id('com.tencent.mm:id/d1k')  # 判断登录注册页面是否打开
        if element.is_displayed():
            end_time = self.get_current_time()
            print 'Activity display: %s' % end_time  # 获取目标页面打开时的时间

        launch_time = end_time - begin_time
        print launch_time

        date = (begin_time, end_time, launch_time)
        self.write_data_into_csv(date)

        self.clear_env()

    # 以2016-01-01 01:01:01.123456格式输出当前时间
    def get_current_time(self):
        return datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f')

    # 建立结果存储的csv文件
    def create_csv_file(self):
        file_name = self.PHONE_NAME + '-' + self.PLATFORM_VERSION + '.csv'
        csv_file = file(file_name, 'ab')
        csv_file.write(codecs.BOM_UTF8)
        writer = csv.writer(csv_file)
        writer.writerow(['begin time', 'end time', 'launch time'])
        self.writer = writer

    # 将时间写入到csv文件
    def write_data_into_csv(self, data):
        self.writer.writerow(data)

if __name__ == '__main__':
    weixin = LaunchTime(app='/Users/ljzhang/Downloads/weixin.apk', appPackage='com.tencent.mm', appActivity='com.tencent.mm.ui.LauncherUI')
    weixin.create_csv_file()

    # 运行十次
    for i in range(10):
        weixin.test_app_start()
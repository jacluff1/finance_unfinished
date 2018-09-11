# import libraries
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import pandas as pd
import numpy as np
import os
import datetime
import pdb

class BROWSER:

    def _GET_CREDENTIALS(self,cred_key):
        return pd.read_csv("config/credentials.csv", index_col='name', dtype='O').loc[cred_key]

    def _OPEN_BROWSER(self):
        print("opening browser...")
        chromedriver    = 'E:/Programs/chromedriver.exe' #where you have the file
        driver          =   webdriver.Chrome(chromedriver)
        driver.implicitly_wait(1)
        driver.maximize_window()
        wait            =   WebDriverWait(driver,10)
        return driver,wait

    def _LOGIN(self,driver,wait,frame_index=None):
        # navigate to web page
        driver.get(self._login.url)
        # switch frames if needed
        if frame_index != None:
            frames  =   driver.find_elements_by_xpath("//iframe")
            driver.switch_to_frame(frames[frame_index])
        # enter in username
        self._GRAB_ELEMENT(driver,wait,'username').send_keys(self._login.username)
        # enter in password
        self._GRAB_ELEMENT(driver,wait,'password').send_keys(self._login.password)
        # submit login info
        self._GRAB_ELEMENT(driver,wait,'login').click()
        # add base url to instance
        self._url['base_url']  =   driver.current_url

    def _GRAB_ELEMENT(self,driver,wait,key):
        try:
            return driver.find_element_by_xpath(self._xpath[key])
        except:
            try:
                return wait.until(EC.visibility_of_element_located((By.XPATH, self._xpath[key])))
            except:
                return driver.find_element_by_xpath(self._xpath[key])

    def _GRAB_ELEMENTS(self,driver,wait,key):
        try:
            return driver.find_elements_by_xpath(self._xpath[key])
        except:
            try:
                return wait.until(EC.visibility_of_elements_located((By.XPATH, self._xpath[key])))
            except:
                return driver.find_elements_by_xpath(self._xpath[key])

    def _SCROLL(self,driver,page_ratio):
        Y       =   page_ratio * 1080 # 1080 for size of HD TV
        driver.execute_script("window.scrollTo(0, %s)" % Y)

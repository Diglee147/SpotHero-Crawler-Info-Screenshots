import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import json
from difflib import SequenceMatcher
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
from datetime import date
import re, itertools
import os
from lxml import etree
import pickle
from selenium.webdriver.chrome.service import Service
from pynput.keyboard import Key, Controller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from subprocess import CREATE_NO_WINDOW
import pyautogui



urlEvent = input("Input The URL TO CRAWL: ")
options = webdriver.ChromeOptions()
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--no-first-run")
options.add_argument("--no-service-autorun")
options.add_argument("--password-store=basic")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("start-maximized")
service=Service("C:\\Users\\Your User\\OneDrive\\Área de Trabalho\\SpotHero Crawler\\chromedriver.exe")
service.creationflags = CREATE_NO_WINDOW
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://spothero.com/')   


def Run(driver, urlEvent):
        
        def createFolder(directory):
            try:
                if not os.path.exists(directory):
                    os.makedirs(directory)
            except OSError:
                print ('Error: Creating directory. ' +  directory)

        treatedinfo = []
        screenshot_number = 1
        city = ""
        
        def xpath_soup(elemental):
            components = []
            child = elemental if elemental.name else elemental.parent
            for parent in child.parents:
                siblings = parent.find_all(child.name, recursive=False)
                components.append(
                    child.name
                    if siblings == [child] else
                    '%s[%d]' % (child.name, 1 + siblings.index(child))
                    )
                child = parent
            components.reverse()
            return '/%s' % '/'.join(components)
        
        def Get_Event(driver, urlEvent, treatedinfo, screenshot_number):
                driver.get(urlEvent)
                try:
                        continue_anyway = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div/button')))
                        continue_anyway.click()
                except:
                        pass
                time.sleep(random.uniform(1.93,2.17))
                try:
                        result_cities = driver.page_source
                        soup_cities = BeautifulSoup(result_cities, 'lxml')
                        city_names = soup_cities.find("div", {"class": "SpotListHeading"})
                        city = city_names.find("span").text
                        createFolder('./'+ city + '/')
                        createFolder('./'+ city + '/Screenshots')
                except:
                        result_cities = driver.page_source
                        soup_cities = BeautifulSoup(result_cities, 'lxml')
                        city_names = soup_cities.find("div", {"class": "css-1q3ahb4"})
                        city = city_names.find("p", {"class": "chakra-text css-fi7oa5"}).text
                        createFolder('./'+ city + '/')
                        createFolder('./'+ city + '/Screenshots')
                #Get mouse position on PyMouse and configure scroll
                pyautogui.moveTo(1126,614,duration=0.5)
                pyautogui.scroll(-500000)
                time.sleep(random.uniform(0.73,0.87))
                pyautogui.scroll(-500000)
                time.sleep(random.uniform(2.93,3.17))
                
                def clean(s):
                    return re.sub(r'\D', '', s)
                
                resulter = driver.page_source
                souper = BeautifulSoup(resulter, 'lxml')
                Garages_Options = souper.findAll("div", {"class": "FacilitySummary css-geclt6"}) #Look for Garages Options in this area to Expand
                for s in Garages_Options:
                        result_numbers = 0
                        spans = ""
                        result_details = ""
                        soup_details = ""
                        page_item = ""
                        email_grab = ""
                        email = ""
                        new_option = s.find("button", {"class": "chakra-button show-details hide-on-mobile css-drm4lm"})
                        xpathatual = xpath_soup(new_option)
                        time.sleep(random.uniform(0.33,0.47))
                        Garage_Option = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpathatual)))
                        Garage_Option.click()
                        time.sleep(random.uniform(1.95,2.17))
                        resultx = driver.page_source
                        soupx = BeautifulSoup(resultx, 'lxml')
                        try:
                                preview_container = soupx.find("button", {"class": "TextButton read-more"})
                                xpathexpand = xpath_soup(preview_container)
                                preview_container_click = driver.find_element("xpath", xpathexpand)
                                actions = ActionChains(driver)
                                actions.move_to_element(preview_container_click).perform()
                                preview_container_click.click()
                                time.sleep(random.uniform(1.55,1.57))
                        except:
                                pass
                        result_details = driver.page_source
                        soup_details = BeautifulSoup(result_details, 'lxml')
                        page_item = soup_details.find("div", {"class": "SpotDetails SpotDetails-showing"})
                        spans = page_item.findAll("span", {"class": ""}) + page_item.findAll("p", {"class": "instructions"})
                        spans = str(spans)
                        result_numbers = list(map(clean, re.findall(r'(?:(?<![a-z])[^\da-z]*\d[^\da-z]*(?![a-z])){10,}', spans, re.I)))
                        email_grab = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', spans)
                        try:
                                email = email_grab.group(0)
                        except:
                                pass
                        resultxy = 0
                        try:
                                if "@" in email and not "@spothero.com" in email:
                                        resultxy = resultxy + 1
                                        if resultxy == 1:
                                                title = soup_details.find("span", {"class": "FacilitySummary-title show-full-title hide-price"}).text
                                                try:
                                                        for k in result_numbers:
                                                                if len(k) == 7 or len(k) == 10 or len(k) == 12:
                                                                        number = str(k)
                                                                else:
                                                                        number = ""
                                                except:
                                                        number = ""
                                                Getting_There = soup_details.find("p", {"class": "instructions"}).text
                                                info = {
                                                'Title' : title,
                                                'Number' : number,
                                                'Email' : email,
                                                'Getting There' : Getting_There,
                                                }
                                                treatedinfo.append(info)
                                                #Get mouse position on PyMouse and configure scroll
                                                pyautogui.moveTo(779,678,duration=0.5)
                                                pyautogui.scroll(1000000)
                                                pyautogui.scroll(-500)
                                                myScreenshot = pyautogui.screenshot()
                                                myScreenshot.save(r'C:\\Users\\Your User\\OneDrive\\Área de Trabalho\\SpotHero Crawler\\' + city + '\\ScreenShots\\screenshot_' + str(screenshot_number) + '.png')
                                                pyautogui.scroll(-500)
                                                screenshot_number = screenshot_number + 1
                                                myScreenshot = pyautogui.screenshot()
                                                myScreenshot.save(r'C:\\Users\\Your User\\OneDrive\\Área de Trabalho\\SpotHero Crawler\\' + city + '\\ScreenShots\\screenshot_' + str(screenshot_number) + '.png')
                                                pyautogui.scroll(-500)
                                                screenshot_number = screenshot_number + 1
                                                myScreenshot = pyautogui.screenshot()
                                                myScreenshot.save(r'C:\\Users\\Your User\\OneDrive\\Área de Trabalho\\SpotHero Crawler\\' + city + '\\ScreenShots\\screenshot_' + str(screenshot_number) + '.png')
                                                pyautogui.scroll(-500)
                                                screenshot_number = screenshot_number + 1
                                                myScreenshot = pyautogui.screenshot()
                                                myScreenshot.save(r'C:\\Users\\Your User\\OneDrive\\Área de Trabalho\\SpotHero Crawler\\' + city + '\\ScreenShots\\screenshot_' + str(screenshot_number) + '.png')
                                                screenshot_number = screenshot_number + 1
                                else:
                                        email = ""
                                        for k in result_numbers:
                                            if len(k) == 7 or len(k) == 10 or len(k) == 12:
                                                    resultxy = resultxy + 1
                                                    if resultxy == 1:
                                                            title = soup_details.find("span", {"class": "FacilitySummary-title show-full-title hide-price"}).text
                                                            number = str(k)
                                                            Getting_There = soup_details.find("p", {"class": "instructions"}).text
                                                            info = {
                                                            'Title' : title,
                                                            'Number' : number,
                                                            'Email' : email,
                                                            'Getting There' : Getting_There,
                                                            }
                                                            treatedinfo.append(info)
                                                            #Get mouse position on PyMouse and configure scroll
                                                            pyautogui.moveTo(779,678,duration=0.5)
                                                            pyautogui.scroll(1000000)
                                                            pyautogui.scroll(-500)
                                                            myScreenshot = pyautogui.screenshot()
                                                            myScreenshot.save(r'C:\\Users\\Your User\\OneDrive\\Área de Trabalho\\SpotHero Crawler\\' + city + '\\ScreenShots\\screenshot_' + str(screenshot_number) + '.png')
                                                            pyautogui.scroll(-500)
                                                            screenshot_number = screenshot_number + 1
                                                            myScreenshot = pyautogui.screenshot()
                                                            myScreenshot.save(r'C:\\Users\\Your User\\OneDrive\\Área de Trabalho\\SpotHero Crawler\\' + city + '\\ScreenShots\\screenshot_' + str(screenshot_number) + '.png')
                                                            pyautogui.scroll(-500)
                                                            screenshot_number = screenshot_number + 1
                                                            myScreenshot = pyautogui.screenshot()
                                                            myScreenshot.save(r'C:\\Users\\Your User\\OneDrive\\Área de Trabalho\\SpotHero Crawler\\' + city + '\\ScreenShots\\screenshot_' + str(screenshot_number) + '.png')
                                                            pyautogui.scroll(-500)
                                                            screenshot_number = screenshot_number + 1
                                                            myScreenshot = pyautogui.screenshot()
                                                            myScreenshot.save(r'C:\\Users\\Your User\\OneDrive\\Área de Trabalho\\SpotHero Crawler\\' + city + '\\ScreenShots\\screenshot_' + str(screenshot_number) + '.png')
                                                            screenshot_number = screenshot_number + 1
                                                    else:
                                                            pass
                        except:
                                email = ""
                                for k in result_numbers:
                                    if len(k) == 7 or len(k) == 10 or len(k) == 12:
                                            resultxy = resultxy + 1
                                            if resultxy == 1:
                                                    title = soup_details.find("span", {"class": "FacilitySummary-title show-full-title hide-price"}).text
                                                    number = str(k)
                                                    Getting_There = soup_details.find("p", {"class": "instructions"}).text
                                                    info = {
                                                    'Title' : title,
                                                    'Number' : number,
                                                    'Email' : email,
                                                    'Getting There' : Getting_There,
                                                    }
                                                    
                                                    treatedinfo.append(info)
                                                    #Get mouse position on PyMouse and configure scroll
                                                    pyautogui.moveTo(779,678,duration=0.5)
                                                    pyautogui.scroll(1000000)
                                                    pyautogui.scroll(-500)
                                                    myScreenshot = pyautogui.screenshot()
                                                    myScreenshot.save(r'C:\\Users\\Your User\\OneDrive\\Área de Trabalho\\SpotHero Crawler\\' + city + '\\ScreenShots\\screenshot_' + str(screenshot_number) + '.png')
                                                    pyautogui.scroll(-500)
                                                    screenshot_number = screenshot_number + 1
                                                    myScreenshot = pyautogui.screenshot()
                                                    myScreenshot.save(r'C:\\Users\\Your User\\OneDrive\\Área de Trabalho\\SpotHero Crawler\\' + city + '\\ScreenShots\\screenshot_' + str(screenshot_number) + '.png')
                                                    pyautogui.scroll(-500)
                                                    screenshot_number = screenshot_number + 1
                                                    myScreenshot = pyautogui.screenshot()
                                                    myScreenshot.save(r'C:\\Users\\Your User\\OneDrive\\Área de Trabalho\\SpotHero Crawler\\' + city + '\\ScreenShots\\screenshot_' + str(screenshot_number) + '.png')
                                                    pyautogui.scroll(-500)
                                                    screenshot_number = screenshot_number + 1
                                                    myScreenshot = pyautogui.screenshot()
                                                    myScreenshot.save(r'C:\\Users\\Your User\\OneDrive\\Área de Trabalho\\SpotHero Crawler\\' + city + '\\ScreenShots\\screenshot_' + str(screenshot_number) + '.png')
                                                    screenshot_number = screenshot_number + 1
                                            else:
                                                    pass
                df = pd.DataFrame(treatedinfo)
                df.to_excel(f'C:\\Users\\Your User\\OneDrive\\Área de Trabalho\\SpotHero Crawler\\' + city + '\\informations.xlsx')
        
        Get_Event(driver, urlEvent, treatedinfo, screenshot_number)
        

Run(driver, urlEvent)



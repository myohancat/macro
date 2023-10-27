#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time
import datetime
import sys

#########################################################
# CONFIGURE
#########################################################
starttime   = '2023-10-11 16:58:00'
year        = '2023'
month       = '10'
day         = '29'

prefer      = [ 'B-4', 'B-5', 'B-3', 'B-2', 'D-4', 'D-3', 'D-2', 'D-1', 'B-1', 'C-4' ]
##########################################################

if sys.version_info.major == 2:
    driver = webdriver.Chrome(executable_path="driver/118.0.5993.70/chromedriver")
else :
    service = Service(executable_path="driver/118.0.5993.70/chromedriver")
    options = webdriver.ChromeOptions()
    #options.binary_location = r"chrome-linux64/chrome"
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=service, options=options)

def wait(until, before):
	target = datetime.datetime.strptime(until, '%Y-%m-%d %H:%M:%S')
	a = datetime.datetime.now()
	c = target - a
	d = c.total_seconds() - before
	if d > 0:
		time.sleep(d)

def open_reserv_page():
	url = 'https://camping.dpto.or.kr/sub3/3_1.php'
	driver.get(url)
	WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

# WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="btn2"]/a'))).click()
def wait_deck_button(month, day):
    cnt = 0

    while cnt < 10:
        try:
            WebDriverWait(driver, 3).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="calendar_ajax"]/ol/li[contains(.,"'+day+'")]')))
            return button
        except:
            print("Not found. retry : " + str(cnt))
            cnt += 1
            time.sleep(0.2)
        return None
        
def get_deck_list():
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//div[@id="map_ajax"]/div')))
    try:
        button_list = driver.find_elements(By.XPATH, '//a[contains (@onclick, "siteInfoLoad")]')
        return button_list
    except:
        return None

##########################################################
# Main
##########################################################

print("Wait to " + starttime + " before 15.0")
wait(starttime, 15.0)

open_reserv_page()

print("Wait to " + starttime)
wait(starttime, 0.0)

driver.refresh()

button = wait_deck_button(month, day)
if button == None:
    print("No deck button available")
    quit()

button.click()

deck_list = get_deck_list()

# W/A Code for Invalid Deck Issue
if deck_list == None or len(deck_list) == 0:
	open_reserv_page()
	button = wait_deck_button(month, day)
	if button == None:
		print("No deck button available")
		quit()
	button.click()
	deck_list = get_deck_list()

if deck_list == None or len(deck_list) == 0:
	print("No available deck")
	quit()

deck_s = None
end = len(prefer)

for d in deck_list:
	for i in range(0, end):
		if d.text == prefer[i]:
			deck_s = d
			end = i
			break

if deck_s == None:
	for d in reversed(deck_list):
		deck_s = d
		break;
		
if deck_s == None:
	print("No available deck");
	quit()

deck_s.click();

# Select Person
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "person")))
sel_list = driver.find_elements(By.XPATH, '(//select[starts-with(@name, "person")])')
for sel in sel_list:
    select = Select(sel)
    select.select_by_visible_text('2명')

driver.find_element(By.XPATH, '//input[@value="다음단계"]').click()

# Final
WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "or_name")))
driver.find_element(By.XPATH, "//input[@id='rrrname']").send_keys("김경인")
driver.find_element(By.XPATH, "//input[@id='camping_type']").click()
sel_list = driver.find_elements(By.XPATH, '(//select[@id="hp1"])')
for sel in sel_list:
    select = Select(sel)
    select.select_by_visible_text('010')
driver.find_element(By.XPATH, "//input[@id='hp2']").send_keys("7278")
driver.find_element(By.XPATH, "//input[@id='hp3']").send_keys("9276")
sel_list = driver.find_elements(By.XPATH, '(//select[@name="birth_year"])')
for sel in sel_list:
    select = Select(sel)
    select.select_by_visible_text('1979')
sel_list = driver.find_elements(By.XPATH, '(//select[@name="birth_month"])')
for sel in sel_list:
    select = Select(sel)
    select.select_by_visible_text('04')

driver.find_element(By.XPATH, "//input[@name='area']").send_keys("성남")
driver.find_element(By.XPATH, "//input[@id='carnum']").send_keys("20너6520")
driver.find_element(By.XPATH, "//input[@name='agree']").click()
driver.find_element(By.XPATH, "//input[@name='agree2']").click()

driver.find_element(By.XPATH, '//input[@value="다음단계"]').click()

# Account
WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "account_birth")))
driver.find_element(By.XPATH, "//input[@id='account_birth']").send_keys("19790409")
driver.find_element(By.XPATH, "//input[@id='select_hp_1']").send_keys("7278")
driver.find_element(By.XPATH, "//input[@id='select_hp_2']").send_keys("9276")
driver.find_element(By.XPATH, "//input[@id='escw_terms_agree']").click()

# Account
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "naxIfr")))
iframe = driver.find_element(By.XPATH, '//iframe[@id="naxIfr"]')
driver.switch_to.frame(iframe);
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "account_birth")))
driver.find_element(By.XPATH, "//input[@id='account_birth']").send_keys("19790409")
driver.find_element(By.XPATH, "//input[@id='select_hp_1']").send_keys("7278")
driver.find_element(By.XPATH, "//input[@id='select_hp_2']").send_keys("9276")


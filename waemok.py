#!/usr/bin/env python
# -*- coding: utf-8,euc-kr -*-

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
starttime   = '2023-10-31 16:00:00'
year        = '2023'
month       = '11'
day         = '16'

prefer      = [ '왜목-1',  '왜목-2', '왜목-3', '왜목-7', '왜목-6', '왜목-5', '왜목-4']
##########################################################

#chrome_version = "101.0.4951.41"
chrome_version = "118.0.5993.70"

if sys.version_info.major == 2:
    driver = webdriver.Chrome(executable_path="driver/" + chrome_version + "/chromedriver")
else :
    service = Service(executable_path="driver/" + chrome_version + "/chromedriver")
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
    url = 'https://camping.dpto.or.kr/sub3/3_3.php'
    driver.get(url)
    WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

def select_month():
    m = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="calendar_ajax"]/div/ul/li[2]')))
    if m.text != year + "." + month:
        li = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li[@class="cal_next"]')))
        li.find_element(By.TAG_NAME, "a").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li[text()="' + year + '.' + month + '"]')))
    #driver.execute_script("calendarLoad('"+year+"', '"+month+"')")
    
def wait_day_button(month, day):
    ol = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//ol[@class="date"]')))
    days = driver.find_elements(By.XPATH, '//li[starts-with(@onclick, "Mapload")]')
    for d in days:
        try:
            if d.find_element(By.TAG_NAME, "span").text == day:
                return d
        except:
            print("")

    return None
        
def get_deck_list():
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="map_ajax"]/div')))
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
select_month()

button = wait_day_button(month, day)
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
driver.find_element(By.XPATH, "//input[@name='or_name']").send_keys("김경인")
driver.find_element(By.XPATH, "//input[@name='camping_type']").click()
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

driver.find_element(By.XPATH, '//input[@value="다음단계"]').click()

# Account
iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "naxIfr")))
driver.switch_to.frame(iframe);
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='account_birth']")))
driver.find_element(By.XPATH, "//input[@id='account_birth']").send_keys("19790409")
driver.find_element(By.XPATH, "//input[@id='select_hp_1']").send_keys("7278")
driver.find_element(By.XPATH, "//input[@id='select_hp_2']").send_keys("9276")

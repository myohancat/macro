#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import datetime
import sys

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

def login():
	url = 'https://www.chuamautocamping.or.kr/member/login.htm'
	driver.get(url)
	WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
	driver.find_element(By.XPATH, "//input[@id='userid']").send_keys("myohancat")
	driver.find_element(By.XPATH, "//input[@id='passwd']").send_keys("whdmsrud2104")
	driver.find_element(By.XPATH, "//input[@title='로그인']").click()

def open_reserv_page(year, month):
	url = 'https://www.chuamautocamping.or.kr/reservation/02.htm?code=&year='+year+'&month='+month+'#body_content'
	driver.get(url)

	cnt = 0
	while cnt < 10:
		try:
			WebDriverWait(driver, 1).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
			WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, '//a[contains (@href, "type='+reserv_type+'&today='+reserv_date+'")]'))).click()
			break
		except:
			if cnt == 10:
				quit()
			print(cnt)
			driver.refresh()
			cnt += 1
			time.sleep(0.1)

def find_deck(prefer):
	a_select = None
	a_list = driver.find_elements(By.XPATH, '//a[contains (@href, "javascript:area_act")]')
	end = len(prefer)
	for a in a_list:
		for i in range(0, end):
			s = str(a.get_attribute('href'))
			site = s[s.find(',')+2:s.find(')')-1]
			if site == prefer[i]:
				a_select = a
				end = i
				break

	return a_select

#########################################################
# CONFIGURE
#########################################################
starttime   = '2021-09-14 14:00:00'
year        = '2021'
month       = '11'
day         = '04'

prefer      = [ '28', '29', '31', '30', '32', '13', '14', '15', '16', '17', '25', '26', '27', '1', '2', '3', '4' ]

reserv_type = 'car'
reserv_month = '%04d. %02d'%(int(year), int(month))
reserv_date  = '%04d-%02d-%02d'%(int(year), int(month), int(day))
##########################################################


print("Wait to " + starttime + " before 10.0")
wait(starttime, 10.0)

login()

print("Wait to " + starttime)
wait(starttime, 0.0)

open_reserv_page(year, month)

# 1박 2일
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@id="res_For1"]'))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[contains (@href, "javascript:area_act")]')))

deck = None
cnt = 0
while cnt < 10:
	try:
		deck = find_deck(prefer)
		break
	except:
		print(">>>> Exception <<<<<")
		time.sleep(0.1)
		cnt += 1

if deck == None:
	print("Not found")
	quit()
else:
	print("!!!!Found !!!!")

deck.click()

driver.find_element(By.XPATH, "//select[@name='res_Many']/option[text()='1명']").click()
cnt = 0
while cnt < 10:
	try:
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[contains (@href, "javascript:sendit();")]'))).click()
		break
	except:
		cnt += 1
		time.sleep(timeToSleep)

WebDriverWait(driver, 5).until(EC.alert_is_present())
driver.switch_to.alert.accept()

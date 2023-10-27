# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import datetime

driver = webdriver.Chrome(executable_path="driver/118.0.5993.70/chromedriver")

def wait(until, before):
	target = datetime.datetime.strptime(until, '%Y-%m-%d %H:%M:%S')
	a = datetime.datetime.now()
	c = target - a
	d = c.total_seconds() - before
	if d > 0:
		time.sleep(d)

def open_reserv_page():
	url = 'https://camping.gtdc.or.kr/DZ_reservation/reserCamping_v3.php?xch=reservation&xid=camping_reservation&sdate=' + reserv_month
	driver.get(url)
	WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

def close_popup():
	click = driver.find_element(By.NAME, value="today_dpnone")
	click.click()

	click2 = driver.find_element(By.XPATH, '//button[text()="동의"]')
	click2.click();

def wait_deck_button(deck, reserv_date):
	cnt = 0
	while cnt < 10:
		try:
			WebDriverWait(driver, 3).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
			button = driver.find_element(By.XPATH, '//button[@value="'+ deck + ':'+ reserv_date +'"]')
			return button
		except:
			print("Not found. retry : " + str(cnt))
			cnt += 1
			time.sleep(0.2)
			driver.refresh()
	return None
		
def get_deck_list(deck, reserv_date):
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "camping_zone")))
	try:
		button_list = driver.find_elements(By.XPATH, '(//button[@class="areacode deck' + deck + ' on"])')
		return button_list
	except:
		return None
		

#########################################################
# CONFIGURE
#########################################################
starttime   = '2021-12-01 10:00:00'
year        = '2023'
month       = '10'
day         = '21'
#deck        = 'A'
#prefer      = [ 'A141', 'A138', 'A143', 'A139', 'A140', 'A157', 'A156', 'A158', 'A155', 'A154', 
#                'A151', 'A152', 'A153', 'A133', 'A130', 'A135', 'A127', 'A117', 'A115', 'A116', 
#                'A113', 'A114', 'A145', 'A112', 'A111', 'A119', 'A118', 'A134', 'A159', 'A160', 
#                'A161', 'A144', 'A142', 'A147', 'A148', 'A149', 'A150', 'A137', 'A121', 'A123', 
#                'A124', 'A120', 'A125', 'A126', 'A128', 'A129', 'A131', 'A132', 'A122', 'A136', 
#                'A101', 'A102', 'A103', 'A104', 'A105', 'A106', 'A107', 'A108', 'A109', 'A110', 
#                'A146' ]

deck        = 'D'
prefer      = [ 'D702', 'D704', 'D703', 'D701', 'D705', 'D706', 'D707', 'D708', 'D709' ]
reserv_month = '%04d%02d'%(int(year), int(month))
reserv_date  = '%04d-%02d-%02d'%(int(year), int(month), int(day))
##########################################################


##########################################################
# Main
##########################################################

print("Wait to " + starttime + " before 15.0")
wait(starttime, 15.0)


open_reserv_page()

close_popup()

print("Wait to " + starttime)
wait(starttime, 0.0)

driver.refresh()

button = wait_deck_button(deck, reserv_date)
if button == None:
	print("No deck button available")
	quit()

button.click()

deck_list = get_deck_list(deck, reserv_date)

# W/A Code for Invalid Deck Issue
if deck_list == None or len(deck_list) == 0:
	open_reserv_page()
	button = wait_deck_button(deck, reserv_date)
	if button == None:
		print("No deck button available")
		quit()
	button.click()
	deck_list = get_deck_list(deck, reserv_date)

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

# Wait INPUT appRoom[]
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "appRoom[]")))
sel_list = driver.find_elements(By.XPATH, '(//select[starts-with(@name, "selPerson")])')
for sel in sel_list:
	select = Select(sel)
	select.select_by_visible_text('2명')

driver.find_element(By.XPATH, '//button[text()="다음단계"]').click()

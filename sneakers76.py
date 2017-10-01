# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import json
import time
from time import sleep
import random

# TO DO LIST
# 1. TARGET THE FIRST 5 PRODUCTS IN NEW ARRIVALS BECAUSE AS SOON AS TARGET PRODUCT IS LIVE, IT WILL BE AT THE TOP OF PAGE
keywords = "SNOOPY"
targetSize = "US 9 EU 42 "

c = requests.Session()

def Time():
	s = datetime.now()
	t = s.strftime("%a %b %d  %-I:%M:%S:%f")[:-3] + 'ms'
	return t

def main():
	global targetLink

	print Time() + '\t' "FETCHING PRODUCT..."

	while True:
		latestArrivalsREQ = c.get('http://www.sneakers76.com/en/new-products')
		latestArrivalsRESP = BeautifulSoup(latestArrivalsREQ.content, 'lxml')

		counter = 0

		for i in latestArrivalsRESP.find_all('a', attrs = {'class': 'product-name', 'itemprop': True, 'href': True}):
			if keywords in i['title']:
				targetLink = i['href']
				counter = 1

		if counter == 1:
			print Time() + '\t' + "PRODUCT FOUND"
			print targetLink
			break

		if counter == 0:
			print Time() + '\t' + "PRODUCT NOT LIVE"


	productREQ = c.get(targetLink)
	productRESP = BeautifulSoup(productREQ.content, 'lxml')

	token = productRESP.find('input', attrs = {'name': 'token'})['value']
	id_product = productRESP.find('input', attrs = {'name': 'id_product'})['value']

	group_9 = ''
	for size in productRESP.find_all(attrs = {'title': True, 'value': True}):
		if targetSize in size['title']:
			group_9 = size['value']

	test = str(productRESP.find('script', attrs = {'type': 'text/javascript', 'src': '/js/jquery/jquery-1.11.0.min.js'}).find_previous())
	
	container = ''
	for i in test.split(';'):
		if 'combinationsFromController' in i:
			container = i.split('= {')[1]

	group_9 = ''
	for i in container.split('},'):
		if 'attributes_values' in i and targetSize in i:
			group_9 = i.replace('"', '').split(':',1)[0]

	#########################################################################################################################################
	#BEGIN ATC AND CHECKOUT

	atcHEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
					'Accept-Encoding': 'gzip, deflate',
					'Accept-Language': 'en-US,en;q=0.8',
					'Cache-Control': 'max-age=0',
					'Connection': 'keep-alive',
					'Content-Length': '113',
					'Content-Type': 'application/x-www-form-urlencoded',
					'Host': 'www.sneakers76.com',
					'Origin': 'http://www.sneakers76.com',
					'Referer': targetLink,
					'Upgrade-Insecure-Requests': '1',
					'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.83'}

	atcDATA = {'token': token,
				'id_product': id_product,
				'add': '1',
				'id_product_attribute': '28332',
				'group_9': group_9,
				'qty': '1',
				'Submit': ''}

	atcREQ = c.post('http://www.sneakers76.com/en/cart', data = atcDATA, headers = atcHEADERS, allow_redirects = True)
	atcRESP = BeautifulSoup(atcREQ.content, 'lxml')

	

	checkoutStep1HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
							'Accept-Encoding': 'gzip, deflate',
							'Accept-Language': 'en-US,en;q=0.8',
							'Connection': 'keep-alive',
							'Host': 'www.sneakers76.com',
							'Referer': atcREQ.url,
							'Upgrade-Insecure-Requests': '1',
							'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.83'}

	checkoutStep1PARAMS = {'step': '1'}

	checkoutStep1REQ = c.get('http://www.sneakers76.com/en/order', params = checkoutStep1PARAMS, headers = checkoutStep1HEADERS, allow_redirects = True)
	checkoutStep1RESP = BeautifulSoup(checkoutStep1REQ.content, 'lxml')


	
	
	checkoutStep2HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
							'Accept-Encoding': 'gzip, deflate',
							'Accept-Language': 'en-US,en;q=0.8',
							'Cache-Control': 'max-age=0',
							'Connection': 'keep-alive',
							'Content-Length': '117',
							'Content-Type': 'application/x-www-form-urlencoded',
							'Host': 'www.sneakers76.com',
							'Origin': 'http://www.sneakers76.com',
							'Referer': checkoutStep1REQ.url,
							'Upgrade-Insecure-Requests': '1',
							'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.83'}

	checkoutStep2DATA = {'email': 'ricksbricks@yahoo.com',
						'passwd': 'cosita',
						'back': 'http://www.sneakers76.com/en/order?step=1',
						'SubmitLogin': ''}

	checkoutStep2REQ = c.post('http://www.sneakers76.com/en/authentication', data = checkoutStep2DATA, headers = checkoutStep2HEADERS, allow_redirects = True)
	checkoutStep2RESP = BeautifulSoup(checkoutStep2REQ.content, 'lxml')


	id_address_delivery = checkoutStep2RESP.find('option', attrs = {'selected': 'selected'})['value']

	checkoutStep3HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
							'Accept-Encoding': 'gzip, deflate',
							'Accept-Language': 'en-US,en;q=0.8',
							'Cache-Control': 'max-age=0',
							'Connection': 'keep-alive',
							'Content-Length': '69',
							'Content-Type': 'application/x-www-form-urlencoded',
							'Host': 'www.sneakers76.com',
							'Origin': 'http://www.sneakers76.com',
							'Referer': checkoutStep2REQ.url,
							'Upgrade-Insecure-Requests': '1',
							'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.83'}

	checkoutStep3DATA = {'id_address_delivery': id_address_delivery,
						'same': '1',
						'message': '',
						'step': '2',
						'back': '',
						'processAddress': ''}


	checkoutStep3REQ = c.post('http://www.sneakers76.com/en/order', data = checkoutStep3DATA, headers = checkoutStep3HEADERS)
	checkoutStep3RESP = BeautifulSoup(checkoutStep3REQ.content, 'lxml')


	delivery_option = checkoutStep3RESP.find(attrs = {'id': 'delivery_option_6144_0'})['value']

	checkoutStep4HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
							'Accept-Encoding': 'gzip, deflate',
							'Accept-Language': 'en-US,en;q=0.8',
							'Cache-Control': 'max-age=0',
							'Connection': 'keep-alive',
							'Content-Length': '61',
							'Content-Type': 'application/x-www-form-urlencoded',
							'Host': 'www.sneakers76.com',
							'Origin': 'http://www.sneakers76.com',
							'Referer': 'http://www.sneakers76.com/en/order',
							'Upgrade-Insecure-Requests': '1',
							'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.83'}

	checkoutStep4DATA = {'delivery_option[6144]': delivery_option,
						'step': '3',
						'back': '',
						'processCarrier': ''}


	checkoutStep4REQ = c.post('http://www.sneakers76.com/en/order', data = checkoutStep4DATA, headers = checkoutStep4HEADERS)
	checkoutStep4RESP = BeautifulSoup(checkoutStep4REQ.content, 'lxml')

	

	checkoutStep5HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
							'Accept-Encoding': 'gzip, deflate',
							'Accept-Language': 'en-US,en;q=0.8',
							'Cache-Control': 'max-age=0',
							'Connection': 'keep-alive',
							'Content-Length': '111',
							'Content-Type': 'application/x-www-form-urlencoded',
							'Host': 'www.sneakers76.com',
							'Origin': 'http://www.sneakers76.com',
							'Referer': 'http://www.sneakers76.com/en/order',
							'Upgrade-Insecure-Requests': '1',
							'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.83'}

	checkoutStep5DATA = {'express_checkout': 'payment_cart',
						'current_shop_url': 'http://www.sneakers76.com/en/order?',
						'bn': 'PRESTASHOP_EC'}

	checkoutStep5REQ = c.post('http://www.sneakers76.com/modules/paypal/express_checkout/payment.php', data = checkoutStep5DATA, headers = checkoutStep5HEADERS, allow_redirects = True)
	checkoutStep5RESP = BeautifulSoup(checkoutStep5REQ.content, 'lxml')

	checkoutURLTOKEN = str(checkoutStep5REQ.url).split('&token=')[1]

	paypalVarContainer = str(checkoutStep5RESP.find_all('noscript')[-1])

	calc = ''
	csci = ''
	for i in paypalVarContainer.split(';'):
		if "calc" in i:
			calc = i.split('=')[1].split('&')[0]
		if "csci" in i:
			csci = i.split('=')[1].split('&')[0]



	checkoutStep6HEADERS = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
							'accept-encoding': 'gzip, deflate, br',
							'accept-language': 'en-US,en;q=0.8',
							'referer': checkoutStep5REQ.url,
							'upgrade-insecure-requests': '1',
							'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

	checkoutStep6URL = 'https://www.paypal.com/webapps/xoonboarding?token=' + checkoutURLTOKEN + '&country.x=US&locale.x=en_US&country.x=US&locale.x=en_US'
	

	checkoutStep6REQ = c.get(checkoutStep6URL, headers = checkoutStep6HEADERS)




	checkoutStep7HEADERS = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
							"accept-encoding": "gzip, deflate, br",
							"accept-language": "en-US,en;q=0.8",
							"referer": checkoutStep6REQ.url,
							"upgrade-insecure-requests": "1",
							"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}

	checkoutStep7URL = 'https://www.paypal.com/cgi-bin/webscr?cmd=_express-checkout&xo_node_fallback=true&force_sa=true&token=' + checkoutURLTOKEN + '&fallback=1&reason=noscript'
	
	checkoutStep7REQ = c.get(checkoutStep7URL, headers = checkoutStep7HEADERS)
	checkoutStep7RESP = BeautifulSoup(checkoutStep7REQ.content, 'lxml')


	currentSession = checkoutStep7RESP.find('input', attrs = {'id': 'currentSession'})['value']
	currentDispatch = checkoutStep7RESP.find('input', attrs = {'id': 'currentDispatch'})['value']
	SESSION = checkoutStep7RESP.find('input', attrs = {'id': 'pageSession'})['value']
	dispatch = str(checkoutStep7RESP.find('input', attrs = {'id': 'pageDispatch'})['value'])
	CONTEXT = checkoutStep7RESP.find('input', attrs = {'id': 'CONTEXT_CGI_VAR'})['value']
	auth = checkoutStep7RESP.find('input', attrs = {'name': 'auth'})['value']
	rapidsState = checkoutStep7RESP.find('input', attrs = {'name': 'rapidsState'})['value']
	rapidsStateSignature = checkoutStep7RESP.find('input', attrs = {'name': 'rapidsStateSignature'})['value']


	checkoutStep8URL = 'https://www.paypal.com/us/cgi-bin/merchantpaymentweb?dispatch=' + dispatch

	checkoutStep8HEADERS = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
							"accept-encoding": "gzip, deflate, br",
							"accept-language": "en-US,en;q=0.8",
							"cache-control": "max-age=0",
							"content-length": "1054",
							"content-type": "application/x-www-form-urlencoded",
							"origin": "https://www.paypal.com",
							"referer": checkoutStep7REQ.url,
							"upgrade-insecure-requests": "1",
							"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}

	checkoutStep8DATA = {"cmd": "_flow",
						"myAllTextSubmitID": "",
						"miniPager": "",
						"reviewPgReturn": "1",
						"font_option": "font_normal",
						"currentSession": currentSession,
						"pageState": "login",
						"currentDispatch": currentDispatch,
						"flag_non_js": "true",
						"email_recovery": "false",
						"password_recovery": "false",
						"login_email": "ricksbricks@yahoo.com",
						"login_password": "",
						"private_device_checkbox_flag": "on",
						"SESSION": SESSION,
						"dispatch": dispatch,
						"CONTEXT": CONTEXT,
						"new_user_button.x": "Don't have a PayPal account?",
						"cmd": "_flow",
						"id": "",
						"close_external_flow": "false",
						"external_close_account_payment_flow": "payment_flow",
						"auth": auth,
						"rapidsState": rapidsState,
						"rapidsStateSignature": rapidsStateSignature,
						"form_charset": "UTF-8"}


	checkoutStep8REQ = c.post(checkoutStep8URL, data = checkoutStep8DATA, headers = checkoutStep8HEADERS, allow_redirects = True)
	checkoutStep8RESP = BeautifulSoup(checkoutStep8REQ.content, 'lxml')




	
	lastCurrentSession = checkoutStep8RESP.find('input', attrs = {'id': 'currentSession'})['value']
	lastCurrentDispatch = checkoutStep8RESP.find('input', attrs = {'id': 'currentDispatch'})['value']
	lastSESSION = checkoutStep8RESP.find('input', attrs = {'id': 'pageSession'})['value']
	lastPageDispatch = checkoutStep8RESP.find('input', attrs = {'id': 'pageDispatch'})['value']
	lastCONTEXT = checkoutStep8RESP.find('input', attrs = {'id': 'CONTEXT_CGI_VAR'})['value']
	lastAuth = checkoutStep8RESP.find('input', attrs = {'name': 'auth'})['value']
	lastRapidsState = checkoutStep8RESP.find('input', attrs = {'name': 'rapidsState'})['value']
	lastRapidsStateSignature = checkoutStep8RESP.find('input', attrs = {'name': 'rapidsStateSignature'})['value']



	checkoutStep9HEADERS = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
							"accept-encoding": "gzip, deflate, br",
							"accept-language": "en-US,en;q=0.8",
							"cache-control": "max-age=0",
							"content-length": "1609",
							"content-type": "application/x-www-form-urlencoded",
							"origin": "https://www.paypal.com",
							"referer": checkoutStep8REQ.url,
							"upgrade-insecure-requests": "1",
							"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}

	checkoutStep9DATA = {"cmd": "_flow",
						"myAllTextSubmitID": "",
						"miniPager": "",
						"reviewPgReturn": "1",
						"font_option": "font_normal",
						"currentSession": lastCurrentSession,
						"pageState": "billing",
						"currentDispatch": lastCurrentDispatch,
						"refresh_country_code": "0",
						"country_code": "US",
						"cc_brand": "",
						"cc_number": "4859109132740450",	#CARD NUMBER
						"credit_card_type": "V",			#VISA
						"expdate_month": "09",				#MONTH
						"expdate_year": "21",				#YEAR
						"cvv2_number": "272",				#CVV
						"cc_country_code": "US",
						"cc_brand": "",
						"shadow_bank_acct_routing_number": "",
						"shadow_bank_acct_account_number": "",
						"shadow_cc_number": "",
						"first_name": "Abel",				# FIRST NAME
						"last_name": "Garcia",				# LAST NAME
						"address_country_code": "US",		# COUNTRY
						"address1": "9063 Montoya St.",		# ADDRESS 1
						"address2": "Apt. 1",				# ADDRESS 2
						"city": "Sacramento",				# CITY
						"state": "CA",						# STATE
						"zip": "95826",						# ZIPCODE
						"tel_type": "Mobile",
						"H_PhoneNumber": "916-842-7628",	# PHONE NUMBER
						"email": "ricksbricks@yahoo.com",	# EMAIL
						"password": "",
						"retype_password": "",
						"tos": "true",
						"create_password_expanded": "",
						"continue.x": "Review and Continue",
						"signUpButtonLabelexpd": "Agree and Continue",
						"signUpButtonLabelcol": "Review and Continue",
						"back-button-form-fields": "",
						"javascript_enabled": "false",
						"SESSION": lastSESSION,
						"dispatch": lastPageDispatch,
						"pageServerName": "merchantpaymentweb",
						"CONTEXT": lastCONTEXT,
						"cmd": "_flow",
						"id": "",
						"note": "",
						"close_external_flow": "false",
						"external_close_account_payment_flow": "payment_flow",
						"auth": lastAuth,
						"rapidsState": lastRapidsState,
						"rapidsStateSignature": lastRapidsStateSignature,
						"form_charset": "UTF-8"}

	checkoutStep9URL = 'https://www.paypal.com/us/cgi-bin/merchantpaymentweb?dispatch=' + lastCurrentDispatch

	checkoutStep9REQ = c.post(checkoutStep9URL, data = checkoutStep9DATA, headers = checkoutStep9HEADERS, allow_redirects = True)
	checkoutStep9RESP = BeautifulSoup(checkoutStep9REQ.content, 'lxml')



	finalCurrentSession = checkoutStep9RESP.find('input', attrs = {'id': 'currentSession'})['value']
	finalCurrentDispatch = checkoutStep9RESP.find('input', attrs = {'id': 'currentDispatch'})['value']
	finalSESSION = checkoutStep9RESP.find('input', attrs = {'id': 'pageSession'})['value']
	finalDispatch = checkoutStep9RESP.find('input', attrs = {'id': 'pageDispatch'})['value']
	funding_source_id = checkoutStep9RESP.find('input', attrs = {'name': 'funding_source_id'})['value']
	finalCONTEXT = checkoutStep9RESP.find('input', attrs = {'id': 'CONTEXT_CGI_VAR'})['value']
	finalAuth = checkoutStep9RESP.find('input', attrs = {'name': 'auth'})['value']
	finalRapidsState = checkoutStep9RESP.find('input', attrs = {'name': 'rapidsState'})['value']
	finalRapidsStateSignature = checkoutStep9RESP.find('input', attrs = {'name': 'rapidsStateSignature'})['value']



	checkoutStep10HEADERS = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
							"accept-encoding": "gzip, deflate, br",
							"accept-language": "en-US,en;q=0.8",
							"cache-control": "max-age=0",
							"content-length": "950",
							"content-type": "application/x-www-form-urlencoded",
							"origin": "https://www.paypal.com",
							"referer": checkoutStep9REQ.url,
							"upgrade-insecure-requests": "1",
							"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}

	checkoutStep10DATA = {"cmd": "_flow",
						"myAllTextSubmitID": "",
						"miniPager": "",
						"reviewPgReturn": "1",
						"font_option": "font_normal",
						"currentSession": finalCurrentSession,
						"pageState": "review",
						"currentDispatch": finalCurrentDispatch,
						"SESSION": finalSESSION,
						"dispatch": finalDispatch,
						"pageServerName": "merchantpaymentweb",
						"funding_source_id": funding_source_id,
						"CONTEXT": finalCONTEXT,
						"continue": "Continue",
						"auth": finalAuth,
						"rapidsState": finalRapidsState,
						"rapidsStateSignature": finalRapidsStateSignature,
						"form_charset": "UTF-8"}

	checkoutStep10URL = 'https://www.paypal.com/us/cgi-bin/merchantpaymentweb?dispatch=' + finalCurrentDispatch

	print Time() + '\t' "FINALIZING CHECKOUT"
	checkoutStep10REQ = c.post(checkoutStep10URL, data = checkoutStep10DATA, headers = checkoutStep10HEADERS, allow_redirects = True)
	checkoutStep10RESP = BeautifulSoup(checkoutStep10REQ.content, 'lxml')

	print checkoutStep10RESP.prettify()
	print checkoutStep10REQ.url

























main()

# -*- coding: utf-8 -*-
#google search result of company's address and tel
#reference:http://www.jianshu.com/p/a4d13ba26107 
from bs4 import BeautifulSoup
from collections import OrderedDict
import requests
import csv
import urllib
import random
import time




# read parameter file
def read_parameter(file_name):
	result_list = []
	with open(file_name, "r") as f:
		for line in f:
			result_list.append(line.replace("\n", ""))
	
	return result_list



# google search
def search_result(keyword, domain, headers, proxy):	
	url = "https://" + domain + "/search?q=" + urllib.quote(keyword) 
	print url
		
	res = requests.get(url, headers = headers, proxies = proxy, timeout = 10)

	soup = BeautifulSoup(res.text, "html.parser")
	
	#parse company address and tel
	if len(soup.select("._tA")) != 0:
		address = soup.select("._tA")[0].text.encode("big5").strip()
		tel = soup.select("._tA")[1].text.encode("big5").replace("+886 ", "0").strip()
	else:
		address = ""
		tel = ""

	return address, tel



if __name__ == "__main__":

	# keep same order of company
	company = OrderedDict()
	
	# search company name
	with open("company name.csv", "r") as f:
		reader = csv.reader(f, delimiter = ",")
		next(reader, None)  # ignore column name
		for i in reader:
			company[i[1]] = [i[0], i[2], i[3], i[4]]


	USER_AGENT = read_parameter("user_agents.txt")  # get user_agent list
	DOMAIN = read_parameter("all_domain.txt")  # get domain list
	PROXY = read_parameter("proxies.txt")  # get proxy list


	#save data
	data = []
	data.append(["GUI", "company", "address_ori", "address_google", "tel_ori1", "tel_ori2", "tel_google"])

	proxy = random.choice(PROXY)
	proxy = {"http":proxy}
	user_agent = random.choice(USER_AGENT)
	domain = random.choice(DOMAIN)
	headers = {"accept-language":"zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4", 
			   "user-agent":user_agent}

	count = 0
	for keyword in company.keys():
		while True:
			try:
				address, tel = search_result(keyword, domain, headers, proxy)
			except:
				with open("result.csv", "ab") as f:
					w = csv.writer(f)
					w.writerows(data)
					data = []

				user_agent = random.choice(USER_AGENT)
				domain = random.choice(DOMAIN)
				headers = {"accept-language":"zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4", 
						   "user-agent":user_agent}
				continue
			break


		#GUI, company, address_ori, address_google, tel_ori1, tel_ori2, tel_google
		data.append([company[keyword][0], keyword, company[keyword][1], address, company[keyword][2], company[keyword][3], tel])

		#every 5 times sleep 1~3 seconds randomly
		if count%5 == 0:
			time.sleep(random.randint(1, 3))
		count = count + 1



	with open("result.csv", "ab") as f:
		w = csv.writer(f)
		w.writerows(data)





from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.proxy import Proxy, ProxyType

import time
import random

import pandas as pd
import re

#  webdriver setup

PORT = '10001'
HOSTNAME = 'us.smartproxy.com'


def configureProxy(): # 6
    p = Proxy() # 7
    p.proxy_type = ProxyType.MANUAL
    p.http_proxy = '{hostname}:{port}'.format(hostname = 
                      HOSTNAME, port = PORT)
    p.ssl_proxy = '{hostname}:{port}'.format(hostname = 
                      HOSTNAME, port = PORT) # 8

    capabilities = webdriver.DesiredCapabilities.CHROME
    p.add_to_capabilities(capabilities) # 9
    return capabilities

options = Options()
options.add_argument('--no-sandbox')
options.add_argument("--headless")
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

df= pd.read_csv("/Users/ruchiraray/Documents/UT CML/Cleaned (without citation).csv" )

# run from 149 to 250 in batches and also save these batches in seperate csv. If the terminal prints "Please show you're not a robot" or "Our systems have detected unusual traffic from your computer network. This page checks to see if it's really you sending the requests, and not a robot. Why did this happen?" you have to stop for a while or change your network

df=df[407:450]
# print(df)

# quit()
#open the webpage
for i, row in df.iterrows():
    k=row['Title']
    # k="A message from Addiction's new Editor‐in‐Chief, Professor John Marsden."
    query = re.sub(r"[^a-zA-Z0-9]+", ' ', k)
    print(query)
    # query = "A message from Addiction s new Editor in Chief Professor John Marsden"
    url = "https://scholar.google.com/scholar?hl=en&q="+query
    driver.get(url)
    
    # driver.get("https://www.geeksforgeeks.org/competitive-programming-a-complete-guide/")
    # print(driver.find_element(By.XPATH, "/html/body").text)
    x=driver.find_element(By.XPATH, "/html/body").text
    print(x)


    # quit()
  
    # print("sk")

    time.sleep(3)
    elements = [f for f in driver.find_elements(By.XPATH, "//*[contains(@class, 'gs_fl') or @class = 'gs_fl']")]
    if len(elements) > 2:
        df.at[i,"Citation"]="-"
        print("putting a -")
        continue;

    # quit()

    # wait for the page to load and extract the number of citations
    time.sleep(3)
    try:
        cited_by = driver.find_element(By.XPATH, "//a[contains(text(),'Cited by ')]")
    except:
        df.at[i,"Citation"]=0
        # print(row['Citation'])
        print("putting a 0")
        df.to_csv("/Users/ruchiraray/Documents/UT CML/Withcite8.csv")
        # quit()
        continue;
    else:
        print(cited_by)
        # quit()
        num_citations = cited_by.text.split(" ")[-1]
        print(f"The paper has {num_citations} citations.")
        df.at[i,"Citation"]=num_citations
        # print(row['Citation'])
        df.to_csv("/Users/ruchiraray/Documents/UT CML/Withcite8.csv")
        # quit()

df.to_csv("/Users/ruchiraray/Documents/UT CML/Withcite8.csv")
# close the webdriver
# driver.quit()
driver.close()
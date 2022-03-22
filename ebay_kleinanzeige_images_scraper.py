# -*- coding: utf-8 -*-
"""Ebay_Kleinanzeige_Images_Scraper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hOcuZJ_1B5fV5EHMvxtlfyTGhy_meC1z

# Ebay Kleinanzeige Image Scraper  
### Python script to retrieve images from the ebay kleinanzeige webseite
---
If you want to collect images of IKEA products from Ebay Kleinazeige, first create an ikeaRangeListJson by following the steps 1.1 to 2.4 in this project:
https://github.com/Greqorian/IKEAcom_Image_Scraper
<br/> However, you can scrap pictures of any items you like, just provide your own product list in step 3.2

Scraping images from the Ebay Kleinanzeige Service is done in 3 steps:

# 1. Libraries and constants definition

1.1 Import libraries
"""

# package imports
#basics
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import json # json files

#scrapping
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import time

"""1.2 Define headers to be visible as the Google Bot.
<br/> to not to get blocket by Ebay
"""

# Set up the headers of the request (User-Agent) as Google boot. Otherwise Ebay-Kleinanzeigen blocks requests.
headers = {
      'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
  }

"""1.3 Mount storage"""

from google.colab import drive
drive.mount('/content/drive')

"""# 2. Function definition

2.1 Create BeautifulSoup instance
"""

# gets BeautifulSoup instance from url request
# param url: (string) url adress of the website
def getSoupFromUtl(url):
  
  # saves HTML of the webpage to the variable
  response = requests.get(url, headers=headers)

  # saves the content of the page
  page = response.content

  # creates an instance of BeautifulSoup with webpage content
  soup = BeautifulSoup(page, "html.parser")

  return soup

"""2.2 Creates a list of URL adresses in Ebay Kleinanzeige service of one item"""

# returns the list ofi items url adress pages from kleineanzeige search
# param itemName: (string) name of the item to search 

def getItemsUlrsList(itemName):

  # creates a query of the search in ebay kleineanzeige
  query = "Ikea-" + itemName

  # add the Query to Ebay-Kleinanzeigen URL
  URL = "https://www.ebay-kleinanzeigen.de/s-" + query + "/k0"

  # gets BeautifulSoup instance from url request
  soup = getSoupFromUtl(URL)

  # selects a div element with id
  srchRsltsContent = soup.find("div", id="srchrslt-content")

  # selects all links from selected div
  srchRslts = srchRsltsContent.find_all('a', href=True)

  itemPagesUrls = []

  # save a list of subpages URLs
  for a in srchRslts:
      
      if '/s-anzeige' in a['href']:
        itemPagesUrls.append('https://www.ebay-kleinanzeigen.de' + a['href'])

  return itemPagesUrls

"""2.3 Create a list of images sources"""

# returns a list of sources for all item images
# param itemPagesUrls ( [string] array ) list of items urls
def getItemsImagesSrcList(itemPagesUrls):

  imagesSrcList = []

  for URL in itemPagesUrls:
    
    # gets BeautifulSoup instance from url request
    soupForSubPage = getSoupFromUtl(URL)

    srchRslts2 = soupForSubPage.find_all("div", {"class": "galleryimage-element"})

    # search for images adresses 
    for tag in srchRslts2:
      image = tag.find("img")
      if hasattr(image, 'src'):
        imagesSrcList.append(image['src'])

  return imagesSrcList

"""# 3. Execution

3.1 Open a list of items
<br/>The list must contain id, name and ulr of the products
<br/> If you want to get list of Ikea products follow steps 1.1 to 2.4 in this project: https://github.com/Greqorian/IKEAcom_Image_Scraper
"""

# Opening JSON file
f = open('/content/drive/MyDrive/DATA/furnitureImages/1000-furniture/ikeaRangeList.json', "r")
# a dictionary
ikeaRangeListJson = json.load(f)

print(len(ikeaRangeListJson))

"""3.2 Create a list of ebay items based of the list of items names

INPUT: This loop takes as input the list of products in the form of:

> ikeaRangeListJson[] = [ {
  <br/> id: string
  <br/> name: string
  <br/> url: string
<br/> } ]

RESULT: This loop fills the new list with item id, name and list of urls as follows:

> itemsList[] = [ {
  <br/> id: string
  <br/> name: string
  <br/> urls: string[]
  <br/> imgSrcs: string[]
<br/> } ]




"""

itemsList = []

for item in ikeaRangeListJson:
  itemsList.append({'id': item['id'], 'name': item['name'], 'urls': getItemsUlrsList(item['name']), 'imgSrcs': []}

"""3.3 Fill list itemsList with images urls from Ebay Kleinanzeige

RESULT: This loop fills the itemsList with item images sources as follows:

> itemsList[] = [ {
  <br/> id: string
  <br/> name: string
  <br/> urls: string[]
  <br/> imgSrcs: string[]
<br/> } ]


"""

for item in itemsList:
  item['imgSrcs'] = getItemsImagesSrcList(item['urls'])
  # wait 10 seconds to not to block the requests by ebay 
  time.sleep(10)

print(itemsList)

"""3.4 Change directory to save the itemsList (optional)"""

os.chdir('/content/drive/MyDrive/DATA/furnitureImages/100-furniture')
!pwd

"""3.5 Save the list of IKEA Products to JSON file (optional)"""

# save the itemslist to JSON file
with open('ebayItemsList.json', 'w', encoding='utf-8') as outfile:
    json.dump(itemsList, outfile, ensure_ascii=False)

"""3.5 Set your train ditrectory to save download images """

os.chdir('/content/drive/MyDrive/DATA/furnitureImages/100-furniture/train')
!pwd

"""3.6 Scrape images to selected directory and create list of labels"""

# list for images labels
ebayImagesList = []

for item in itemsList:
  # some symbols cannot be saved to the name of file, make sure they are replaced
  name = item['name'].replace('/', '_')
  id = item['id']

  for index, src in enumerate(item['imgSrcs']):
    fileName = str(index) + '_' + id + '_' + name + '_' + 'ebay' +'.jpg'
    ebayImagesList.append({'title': fileName, 'name':name})

    with open(fileName, 'wb') as f:
      im = requests.get(src, headers)
      f.write(im.content)
      f.close()
      print('Writing: ', fileName)
print(ebayImagesList)

"""3.7 Save list of labels to JSON file. Important for AI Model training"""

# change directory for the labels list
os.chdir('/content/drive/MyDrive/DATA/furnitureImages/100-furniture/')
!pwd
# save the ebayImagesList to JSON file
with open('ebayImagesList.json', 'w', encoding='utf-8') as outfile:
    json.dump(ebayImagesList, outfile, ensure_ascii=False)
#! /Users/mikeyb/Applications/python3



import requests, os, bs4, sys, shutil
from apiclient import discovery
import httplib2
from selenium import webdriver

DOWNLOAD_FOLDER = '/Users/mikeyb/Downloads/galesburg/'

if len(sys.argv) > 1:
	urlFileInput = sys.argv[1]
else:
	print ('Provide file with URLs to process as argument')
	quit()
	
urlFile = open(urlFileInput,'r')
urls = urlFile.readlines()
imageUrls = []
browser = webdriver.Firefox()

for pageUrl in urls:
	tagAttr = 'content'
	browser.get(pageUrl)
	try:
		# Read meta tages with attribute itemprop equal to image
		rowElem = browser.find_element_by_xpath('//meta[@itemprop="image"]')
		imageUrls.append(rowElem.get_attribute(tagAttr))
		print(rowElem.get_attribute(tagAttr))
	except Exception:
		# If there is an exception write the URL that was skipped
		print('skipped ' + pageUrl)

print('--------------------')
for j in range(0, len(imageUrls)):
	print(imageUrls[j])

# Loop through image URLs and save the image at each
for imgUrl in imageUrls:
	res = requests.get(imgUrl)
	imageFile = open(os.path.join(DOWNLOAD_FOLDER,os.path.basename(imgUrl)),'wb')
	for chunk in res.iter_content(100000):
		imageFile.write(chunk)
	imageFile.close()

browser.quit()


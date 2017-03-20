#- Download only the images in posts -- no banners etc.
#- Any links with text 'something.jpg' or 'something.png' or 'something.gif', map to post date string
#- Then run through Tesseract to discard any images which are obviously not infographs (reject all but V3)
#- Generate a timestamp from the post date text
#- Generate an image hash using SHA or whatever
#- Rename each file with the hash followed by a hyphen and the timestamp
#- Script also automatically adds thread number to a text file, so that the images can be downloaded by others
#I also don't want to download the default image

#class ChartDownloader
import os
import urllib.request
from bs4 import BeautifulSoup

#download all non-gif images from the thread (no animated images)
#user agent spoofing required for desuarchive, possibly others
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

imageExtensions=['jpg','png']
#set your url here: url=
headers={'User-Agent':user_agent,}

assembledRequest = urllib.request.Request(url,None,headers)
soup = BeautifulSoup(urllib.request.urlopen(assembledRequest),'lxml')

opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent',user_agent)]
urllib.request.install_opener(opener)

imageNumber = 0
for link in soup.findAll('a'):
	for extension in imageExtensions:
		if link.text.lower().endswith(extension):
			imageUrl = link.get('href')
			imageNumber+=1
			urllib.request.urlretrieve(imageUrl, str(imageNumber))
			break



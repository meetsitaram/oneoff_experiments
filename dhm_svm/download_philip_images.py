import urllib.request
from bs4 import BeautifulSoup
import time
import os
from random import shuffle

imagesDirectory = './images/'

weburl = 'http://philip.greenspun.com'
imgRootUrl = weburl+"/images/"
print ('Parsing image root directory %s' % imgRootUrl)
html = urllib.request.urlopen(imgRootUrl).read()
#print (html)

soup = BeautifulSoup(html, 'lxml')

imageDirectories = []
for link in soup.findAll('a'):

    imgLink = str(link.get('href'))
    if not imgLink.startswith('/images/'):
        continue
    print (link.get('href'))    
    
    imageDirectories.append(imgLink)

print ('Found %d image directories' % len(imageDirectories))

print ('fetching image links')
jpgLinks = []
    
print ('random shuffling image directories')
shuffle(imageDirectories)

cntDirectories = 5
for imgDir in imageDirectories:
    imgDirUrl = weburl + imgDir +'/'
    
#    if imgDir != '/images/20090920-rachel':
#        continue

#    if imgDir != '/images/200007-ayers-rock-and-olgas':
#        continue
    
    cntDirectories = cntDirectories - 1
    if cntDirectories < 0:
        break
    
    print ('Processing url %s' % imgDirUrl)
    try:
        html = urllib.request.urlopen(imgDirUrl).read()
        soup = BeautifulSoup(html, 'lxml')
    except:
        continue
      
    numImagesPerDir = 200
    for link in soup.findAll('a'):
        hrefLink = str(link.get('href'))
        print (hrefLink)
        
        if hrefLink.endswith('.jpg') and not hrefLink.endswith('thumb.jpg'):
            numImagesPerDir = numImagesPerDir - 1
            if numImagesPerDir < 0:
                break
            jpgLinks.append(hrefLink)

    for link in soup.findAll('img'):
        imgLink = str(link.get('src'))
        print (imgLink)
        
        if imgLink.endswith('.jpg') and not imgLink.endswith('thumb.jpg'):
            numImagesPerDir = numImagesPerDir - 1
            if numImagesPerDir < 0:
                break
            jpgLinks.append(imgLink)
        
        
      
cnt = 0            
for link in jpgLinks:
    
    tokens = link.split('/')
    if len(tokens) < 2:
        print ('ERROR: tokens shortage: %d' % len(tokens))
        continue
    
    imgFileName = tokens[len(tokens)-1]
    imgSubDir = imagesDirectory + tokens[len(tokens) -2]    
    imgFilePath = imgSubDir + '/' + imgFileName                   
    
    if not os.path.exists(imgSubDir):
        print ('creating sub directory %s' % imgSubDir)
        os.makedirs(imgSubDir)
    
    url = weburl + link
    print (url, imgFilePath) 
    try:    
        img = urllib.request.urlopen(url).read()
        outFile = open(imgFilePath,"wb")
        outFile.write(img)
        outFile.close()   
    except:
        print ('ERROR: Failed to download/save img: %s' % url)
        continue
    
    cnt = cnt + 1
    if cnt % 100 == 0:
        print ('dowloaded %d images so far:' % cnt)
        time.sleep(5)
        
        
print ('Total jpg links download: %d' % len(jpgLinks))

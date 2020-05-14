import json
import logging
import os
import urllib.request

from ConnectionManager import PrntScreenManager

file_object = open('C:\\Users\\Neueda\\PycharmProjects\\PrntScrnCrawler\\seenbefore.txt', 'r')
seenbefore = json.load(file_object)

counter = 0
logging.basicConfig(level=logging.DEBUG)

logging.info("Starting application")

logging.info("Starting a image number {}".format(len(seenbefore)))

def main():
    try:
        pscreen = PrntScreenManager()
        for x in range(1,9999):
            url = pscreen.generateurl()
            if url in seenbefore:
                logging.info("URL {} already logged, skipping".format(url))
                continue
            webpage = pscreen.getwebpage(url)
            imgurLink = pscreen.getimgururl(webpage)
            seenbefore.update({url: imgurLink})
            logging.info("Imgur link is {}".format(imgurLink))
            if isinstance(imgurLink, ValueError):
                logging.error("Image Missing, {}".format(imgurLink))
                break
            basepath = "C:\\Users\\Neueda\\PycharmProjects\\PrntScrnCrawler\\images\\"
            filename = imgurLink.split("/")[-2].strip('"')
            urllib.request.urlretrieve(imgurLink, os.path.join(basepath, filename))
    finally:
        print("writing to disk")
        #with open('C:\\Users\\Neueda\\PycharmProjects\\PrntScrnCrawler\\seenbefore.txt', 'w') as file:
        file_object = open('C:\\Users\\Neueda\\PycharmProjects\\PrntScrnCrawler\\seenbefore.txt', 'w')
        json.dump(seenbefore, file_object)

if __name__=='__main__':
    main()
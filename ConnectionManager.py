import logging
import time
import requests
import re

class ConnectionManager:
    def __init__(self):
        self.session = requests.session()
        self.session.headers.update({'User-Agent': 'Custom user agent'})

    def restartconnection(self, url):
        if self.session:
            self.session.close()
        try:
            self.session.get(url)
        except requests.ConnectionError as e:
            time.sleep(60)
            logging.error("Connection to server failed. Failure exception {}".format(e))
            logging.info("Restarting attempting reconnect in 60 seconds")

    def getwebpage(self, url):
        logging.info("Accessing URL: {}".format(url))
        webpage = self.session.get(url)
        try:
            webpage.raise_for_status()
        except:
            logging.error("Connection to server failed, restarting in 60 seconds")
            self.restartconnection(url)
            time.sleep(60)
        time.sleep(1)
        return webpage.content

    def closeconnection(self):
        self.session.close()
        exit(0)

class PrntScreenManager(ConnectionManager):
    counter = 1000
    maxnumber = 9999
    baseurl = 'https://prnt.sc/'
    chars = 'aa'
    pagesAccessed = 0

    def generateurl(self):
        if self.pagesAccessed == 9999:
            exit(0)
        self.counter += 1
        if self.counter > self.maxnumber:
            self._incrementchars()
            self.counter = 1000
        url = self.baseurl + self.chars + str(self.counter)
        if url == 'https://prnt.sc/zz9999':
            logging.info("Max Url has been reached, closing application")
            self.closeconnection()
        return url

    def _incrementchars(self):
        char1, char2 = self.chars[0], self.chars[1]
        if ord(char2) < ord('z'):
            char2 = chr(ord(char2) + 1)
        if ord(char2) == ord('z'):
            char1 = chr(ord(char1) + 1)

        self.chars = str(char1) + str(char2)
        return self.chars

    def getimgururl(self, content):
        imgururl = (re.search(r'(https?://(\w*()i.i*)[^\s]+)', str(content)))
        if 'imgur' not in str(content):
            return 'https://imgur.com/gallery/CZjpqmQ'
        if 'imgur' in imgururl.group(0):
            logging.info("Accessing {}, there have been {} addresses generated in this run".format(imgururl.group(0), self.pagesAccessed))
            self.pagesAccessed += 1
            return imgururl.group(0)
        elif 'image.prntscr' in imgururl.group(0):
            url = imgururl.group(0).split("/")[-1]
            logging.info("Accessing {}, there have been {} addresses generated in this run".format(url, self.pagesAccessed))
            self.pagesAccessed += 1
            return "https://i.imgur.com" + url
        else:
            logging.error("imgur url not found in {}".format(imgururl.group(0)))
            return ValueError

import re
import socket
import string
from urllib2 import urlopen
import urllib2
from htmllib import HTMLParser, HTMLParseError
from urlparse import urlparse, urljoin
from formatter import DumbWriter, AbstractFormatter
from cStringIO import StringIO

from sys import argv


__author__ = 'wengxf'


class Retriever():  # download web pages
    def __init__(self, url):
        self.url = url

    def download(self):  # download web page
        print 'try to open url:', self.url, '\nthe true url process', string.split(self.url, '?')[0]
        try:
            retval = urlopen(string.split(self.url, '?')[0], None, 200)
        except urllib2.HTTPError as e:
            print "HTTPError", e
            return
        except socket.timeout as e:
            print "socket.timeout", e
            return
        except socket.error as e:
            print "socket.error", e
            return
        except urllib2.URLError as e:
            print "URLError: ", e
            return
        return retval

    def parseAndGetLinks(self):  # parse HTML, save links
        self.parser = HTMLParser(AbstractFormatter(DumbWriter(StringIO())))
        r = self.download()
        if r:
            print '________'
            try:
                try:
                    s = r.read(50000)
                except socket.error as e:
                    print "***************************socket error***************************", e
                    return []
                self.parser.feed(s)
                print '------------------'

                r.close()
                print '***************************'
            except HTMLParseError:
                print 'get links error\n'
                return []

        self.parser.close()
        return self.parser.anchorlist


class Crawler(object):  # manage entire crawling process
    count = 0

    def __init__(self, url):
        self.q = [url]
        self.seen = []
        self.dom = urlparse(url)[1]

    def getPage(self, url):
        r = Retriever(url)
        # retval = r.download()
        # if not retval:
        #     return
        # retval.close()
        # if retval[0] == '*':  # error situation , do not parse
        #     print retval, '... skipping parse'
        #     return
        Crawler.count += 1
        print '\n(', Crawler.count, ')'
        print 'URL:', url
       # print 'Content:', retval.read()
        self.seen.append(url)

        links = r.parseAndGetLinks()  # get and process links
        for eachLink in links:
            if eachLink[:4] != 'http' and string.find(eachLink, '://') == -1:
                eachLink = urljoin(url, eachLink)
                print '*', eachLink
                if string.find(string.lower(eachLink), 'mailto:') != -1:
                    print '... discarded, mailto link'
                    continue
                if eachLink not in self.seen:
                    if string.find(eachLink, self.dom) == -1:
                        print '... discarded, not in domain'
                    else:
                        if eachLink not in self.q:
                            self.q.append(eachLink)
                            print '... new , added to Q'
                        else:
                            print '.... discarded, already in Q'
                else:
                    print '... discarded, already processed'

    def go(self):  # process links in queue
        while self.q:
            url = self.q.pop()
            if string.split(url, ':')[0] == 'http'and len(re.findall('//', url)) == 1:
                if len(re.findall('html', url)) < 1:
                    if url[-1] != '/':
                        print 'process utl !/\n', url[-1],  url
                        url += '/index.html'
                    else:
                        print 'process utl /', url
                        url += 'index.html'
                self.getPage(url)


def main():
    if len(argv) > 1:
        url = argv[1]
    else:
        try:
            url = raw_input('Enter starting URL:')
        except(KeyboardInterrupt, EOFError):
            url = ''
    if not url:
        return
    robot = Crawler(url)
    robot.go()


if __name__ == '__main__':
    main()











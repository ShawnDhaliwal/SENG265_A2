#! /opt/bin/python3
# Author: Shawn Dhaliwal, V00811632
#
#


import urllib.request
import urllib.error
import argparse
import re             
import sys

timeout = 1         # 1 second limit on reading a webpage
maxlength = 10000   # max number of bytes to read from a webpage
maxhits = 100       # max number of URLs we will try to open
hits = 0            # number of URL open attempts

def readwebpage( url ):

    global hits, maxhits, timeout, maxlength
    if hits >= maxhits:
        return ""
    hits += 1
    try:
        with urllib.request.urlopen(url, None, timeout) as response:
            bytes = response.read(maxlength)
            return bytes.decode("utf-8")
    except urllib.error.HTTPError:
        return None     # a 404 HTTP error or similar
    except urllib.error.URLError:
        return None     # a 404 HTTP error or similar
    except:
        # it's some other kind of error
        return "Error with URL: "+url

def main():
    global maxhits
    parser = argparse.ArgumentParser(description="Check a website.")
    parser.add_argument('-maxvisits', dest='maxhits', type=int, default=10,
        help="limit the number of url's which will be tested")
    parser.add_argument('url', metavar='url', type=str, nargs=1,
        help='the URL of a website')
    i = 0

    args = parser.parse_args()
    maxhits = args.maxhits
    #Get user specified URL
    url = args.url[0]
    url_list = [url]

    checkedURLs = [url]
    AmountVisited = 0
    print("Checking website ", url)
    badpages = 0
    CheckedSites = 0
    url_list = set(url_list)
    start = url
    dict_webs = {}

    if(maxhits < 0):
        print("ERROR: Number of sites to visit must be greater than Zero")
        sys.exit(0)
    elif(maxhits == 0):
        print("Limit is set to zero, no webpages were visited")
        sys.exit(0)
    elif(maxhits <101):
        print("Maximum number of webpages visits set to ", maxhits)
    else:
        print("Webpage visits allowed is too high, setting to default, 100")
    while (url_list and AmountVisited<maxhits and AmountVisited<100):
        CheckedSites = CheckedSites + 1
        urlParent = url
        url = url_list.pop()
        #Check if URL is working properly
        s = readwebpage(url)
        AmountVisited = AmountVisited + 1
        
        #If URL is not working properly
        if s == None:
            dict_webs[urlParent] = url
            print("* bad reference to ", url, " on ", start )
            badpages = badpages + 1
            
        #Start scanning HTML of the webpage to find other URLs
        else:
            urls_list1 = re.findall(r'href="([\s:]?[^\'" >]+)', s)  
            #print(urls_list1)
            duplicate = urls_list1[:]
            dict_webs[url] = []
            while duplicate:
                dict_webs[url].append(duplicate.pop())
            while urls_list1:
                insert = urls_list1.pop()
                while(insert in checkedURLs and urls_list1):
                    insert = urls_list1.pop()
                while(insert in url_list and urls_list1):
                    insert = urls.list1.pop()
                if urls_list1:
                    url_list.add(insert)
                    checkedURLs.append(insert)
                    

                #print(checkedURLs)
               # print(urls_list1)
    print("Checking finished; ", CheckedSites, "webpages checked; ", badpages, " bad references found")


if __name__ == "__main__":
    main()

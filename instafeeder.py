import feedparser
import urllib 
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

f = open("subscriptions.txt") #Edit subscriptions.txt to add or remove your feed subscriptions
l = f.readlines()

#Instapaper Credentials
username = "YOUR_INSTAPAPER_USERNAME_OR_EMAIL"
password = "YOUR_INSTAPAPER_PASSWORD"
##

add_url = "http://instapaper.com/api/add?"
enc = urllib.urlencode({'username':username, 'password':password})
add_url += enc 

def link_added(feed_url):
    parsed = feedparser.parse(feed_url.strip())
    if 'feedburner_origlink' not in parsed['entries'][0]:
        entry_url = 'link'
    else:
        entry_url = 'feedburner_origlink'
    
    last_added = r.hget(feed_url, "last_added")
    
    i=0
    item =""
    for item in parsed['entries']:
        if str(parsed['entries'][i][entry_url]) != last_added:
            instapaper_url = add_url + '&url='+ str(parsed['entries'][i][entry_url])
            try:
                urllib.urlopen(instapaper_url)
            except IOError:   #Instapaper API seems to give an error sometimes
                urllib.urlopen(instapaper_url) 
    
    return "All items from %s have been added" % feed_url
    

for item in l[:-1]:
    print "Processing %s" % item
    print link_added(item)



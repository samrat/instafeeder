import feedparser
import urllib 
import redis

#r = redis.Redis(host='localhost', port=6379, db=0)

f = open("subscriptions.txt") #Edit subscriptions.txt to add or remove your feed subscriptions
l = f.readlines()
try:
    prev_data_file = open("records.txt")
    prev_data = eval(prev_data_file.read())
    prev_data_file.close()
except: 
    prev_data = {}
    pass

#Instapaper Credentials
username = "YOUR_INSTAPAPER_USERNAME"
password = "YOUR_INSTAPAPER_PASSWORD_(ONLY_IF_YOU_HAVE_ONE)"
##

add_url = "http://instapaper.com/api/add?"
enc = urllib.urlencode({'username':username, 'password':password})
add_url += enc 

def process_feed(feed_url):
    try:
        latest_item_from_feed = prev_data[feed_url]
    except:
        latest_item_from_feed = None
    parsed = feedparser.parse(feed_url.strip())
    if 'feedburner_origlink' not in parsed['entries'][0]:
        entry_url = 'link'
    else:
        entry_url = 'feedburner_origlink'
    
    #last_added = r.hget(feed_url, "last_added")
    
    i=0
    item =""
    for item in parsed['entries']:
        if str(item[entry_url]) != latest_item_from_feed:
            instapaper_url = add_url + '&url='+ str(item[entry_url])
            try:
                urllib.urlopen(instapaper_url)
            except IOError:   #Instapaper API seems to give an error sometimes
                urllib.urlopen(instapaper_url) 
    
    prev_data[feed_url] = str(parsed['entries'][0][entry_url])

    return "All items from %s have been added" % feed_url

for item in l[:-1]:
    print "Processing %s" % item
    print process_feed(item)

write_file = open("records.txt", 'w')
write_file.write(str(prev_data))
write_file.close()


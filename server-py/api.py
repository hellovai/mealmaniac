import random
import urllib2
import json
import datetime

base_url = "https://r-test.ordr.in/"
api_key = "JSxnQl1yk5bIHYUgfubPm6KY4OS_Frwq7-iawxqmoIs"

users = {}
address = {}
card = {}
x = 0

def constructURL(call, fields):
        c = call.split('/')
        for key in fields:
                call = call.replace(key, str(fields[key]))
                # print "\t", call, key
        return base_url + call + "?_auth=1," + api_key

def fill(base, additions):
        for key in additions:
                if key in base:
                        base[key] = additions[key]
        return base

def getAddr(nick):
        if nick not in address:
                address[nick] = {
                                "addr":"625 6th Ave",
                                "city":"New York",
                                "zip":"11215"
                                }
        return address[nick]

def getCard(nick):
        if nick not in card:
                card[nick] = {
                                "number":"1111222233334444"
                                } 
        return card[nick]

def getUser(email):
        if email not in users:
                users[email] = {
                                "id":str(random.randrange(1000000)),
                                "first_name":"John",
                                "last_name":"Doe",
                                "restrictions":"",
                                "phone":"1234567890",
                                "tip":"15",
                                }
        return users[email]

def valid(item):
        today = set([datetime.datetime.now().strftime("%A").lower()])
        other = set(["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]).difference(today)
        t = set(item["name"].lower().split(' '))
        if len(t.intersection(today)) > 0:
                return True
        elif len(t.intersection(other)) > 0:
                return False
        return True        

def checkFlexibility(title):
        bad = set(["choice", "use"])
        good = set(["extra", "extras", "choices"])
        t = set(title.lower().split(' '))
        if len(t.intersection(good)) > 0:
                return True
        elif len(t.intersection(bad)) > 0:
                return False
        return True

def cuisineCheck(cuisines, userid):
        global x
        return True
        x = x + 1
        if x % 5 == 4:
                return True
        return False

def search(addr_nick):
        call = "dl/datetime/zip/city/addr"
        fields = {
                "datetime":"ASAP",
                "addr":"625 6th Ave",
                "city":"New York",
                "zip":"11215"
                }
        fields = fill(fields, getAddr(addr_nick))
        url = constructURL(call, fields)
        data = urllib2.urlopen(url).read()
        return json.loads(data)

def getDetails(rid):
        call = "rd/" + str(rid)
        url = constructURL(call, {})
        data = urllib2.urlopen(url).read()
        return json.loads(data)



import random
import urllib2
import json
import datetime

base_url = "https://r-test.ordr.in/"
api_key = "JSxnQl1yk5bIHYUgfubPm6KY4OS_Frwq7-iawxqmoIs"

email_db = {}
users = {}
restaurants = {}
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

def getAddr(uid,nick):
        if nick not in users[uid]["address"]:
                users[uid]["address"][nick] = {
                                "addr":"625 6th Ave",
                                "city":"New York",
                                "zip":"11215"
                                }
        return users[uid]["address"][nick]

def getCard(uid,nick):
        if nick not in users[uid]["card"]:
                users[uid]["card"][nick] = {
                                "card_name":users[uid]["first_name"] + " " + users[uid]["last_name"],
                                "card_number":"4111111111111111",
                                "card_cvc":"123",
                                "card_expiry":"02/2016",
                                "card_bill_addr":"1 Main Street",
                                "card_bill_city":"College Station",
                                "card_bill_state":"TX",
                                "card_bill_zip":"77840",
                                "card_bill_phone":"2345678901"
                                } 
        return users[uid]["card"][nick]

def getUid(email, pwd):
        if email not in email_db:
                email_db[email] = random.randrange(1000000)
        return email_db[email]

def getUser(uid):
        if uid not in users:
                users[uid] = {
                                "id":uid,
                                "first_name":"John",
                                "last_name":"Doe",
                                "restrictions":"",
                                "phone":"1234567890",
                                "tip":"15",
                                "address":{},
                                "card":{}
                                }
        return users[uid]

def valid(item):
        today = set([datetime.datetime.now().strftime("%A").lower()])
        other = set(["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]).difference(today)
        good = set([])
        bad = set(["beverage", "water", "smoothie", "drink", "alcohol", "alcoholic", "non-alcoholic"])
        t = set(item["name"].lower().split(' '))
        if len(t.intersection(bad)) > 0:
                return False
        elif len(t.intersection(good)) > 0:
                return True
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

def search(uid, addr_nick):
        call = "dl/datetime/zip/city/addr"
        fields = {
                "datetime":"ASAP",
                "addr":"625 6th Ave",
                "city":"New York",
                "zip":"11215"
                }
        fields = fill(fields, getAddr(uid, addr_nick))
        url = constructURL(call, fields)
        data = urllib2.urlopen(url).read()
        return json.loads(data)

def getDetails(rid):
        if rid not in restaurants:
                call = "rd/" + str(rid)
                url = constructURL(call, {})
                restaurants[rid] = urllib2.urlopen(url).read()
        data = restaurants[rid]
        return json.loads(data)

def order():
        return {
                "status":"success"
                }


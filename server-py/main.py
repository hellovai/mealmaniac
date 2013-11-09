import api
import json
from datetime import timedelta
from flask import Flask, make_response, request, current_app
from functools import update_wrapper
import random
import math

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


app = Flask(__name__)

class meal(object):
	"""docstring for meal"""
	def __init__(self, item):
		super(meal, self).__init__()
		self.id = item["id"]
		self.name = item["name"]
		self.price = float(item["price"])
		self.desc = item["descrip"]
		self.rest = -1 if u'rest' not in item else item[u'rest']
		self.options = {}

	def toDict(self):
		res = {
			"id":self.id,
			"name":self.name,
			"price":self.price,
			"desc":self.desc,
			}
		if self.rest != -1:
			rest = api.getDetails(self.rest)
			res["rest"] = {
				"id": self.rest,
				"name": rest["name"],
				"phone": rest["cs_contact_phone"]
				}
		if len(self.options) > 0:
			res["options"] = {}
			for key in self.options:
				option = self.options[key]
				if key not in res["options"]:
					res["options"][key] = []
					for item in option["data"]:
						res["options"][key].append(item.toDict())
		return res

	def addOption(self, key, option, choice=True):
		if key not in self.options:
			self.options[key] = {"flexible":choice, "data":[]}
		self.options[key]["data"].append(option)

	def pickOptions(self, price):
		balance = price - self.price
		copy = meal({"id":self.id, "name":self.name, "price":self.price, "descrip":self.desc, "rest": self.rest})
		for key in self.options:
			option = self.options[key]
			update = []
			used = set()
			for item in option["data"]:
				if item.price <= balance:
					update.append(item)
			if len(update) == 0:
				pick = -1
			else:
				pick = update[random.randrange(len(update))]
				copy.addOption(key, pick)
				balance = balance - pick.price
				used.update(pick.toDict())
			if option["flexible"]:
				ctr = 2
				while pick != -1 and balance > 0:
					update = []
					for item in option["data"]:
						if item.price <= balance and item not in used:
							update.append(item)
					if len(update) == 0 or math.log(ctr)/5.0 < random.random():
						pick = -1
					elif ctr/5.0 < random.random():
						pick = update[random.randrange(len(update))]
						copy.addOption(key, pick)
						balance = balance - pick.price
						ctr = ctr + 1
						used.update(pick.toDict())
					else:
						pick = -1
		return copy, price - balance





		
@crossdomain(origin='*')
@app.route('/')
def hello_world():
    return 'Hoes better download the app'


@crossdomain(origin='*')
@app.route('/address/<uid>/<nick>')
def get_addr(uid, nick):
	return api.get_addr(uid,nick)


@crossdomain(origin='*')
@app.route('/settings/<uid>/<first>/<last>/<address>/<nick>/<phone>/<delivery>/<tip>/<veg>/<gluten>/<allergies>/<card>')
def place_order():
	return api.order()

@app.route('/newcard/<uid>/<cc>/<exp>/<code>')
def add_card(uid, cc, exp, code):
	api.addCard(uid, cc, exp, code)
	return json.dumps({"status":"success"})


@app.route('/newaddress/<uid>/<address>')
def add_addr(uid, street, city, zip):
	api.addCard(uid, street, city, zip)
	return json.dumps({"status":"success"})

@app.route('/login/<email>/<pwd>')
@crossdomain(origin='*')
def login(email, pwd):
	uid = api.getUid(email, pwd)
	user = api.getUser(uid)
	return json.dumps(user)


@app.route('/meal/<uid>/<price>/<nick>')
@crossdomain(origin='*')
def getMeal(uid, price, nick):
	user = api.getUser(uid)
	nearby = api.search(uid, nick)
	price = int(10000 * float(price) / (100 + float(user["tip"]) )) / 100.0 / 1.0875
	# return json.dumps(nearby)
	choices_outer = []
	for rest in nearby:
		if rest["mino"] <= price and rest["is_delivering"] == 1:
			rest_data = api.getDetails(rest["id"])
			choices = []
			addons = []
			if api.cuisineCheck(rest_data["cuisine"], uid):
				for category in rest_data["menu"]:
					for listing in category["children"]:
						if float(listing["price"]) <= price:
							listing["rest"] = rest["id"]
							foodItem = meal(listing)
							if foodItem.price < 4.85 or foodItem.price < 0.6 * price or not api.valid(listing):
								base = addons
							else:
								base = choices
							if "children" in listing:
								for option in listing["children"]:
									if api.valid(option):
										title = option["name"]
										flex = api.checkFlexibility(title)
										if "children" in option:
											for op in option["children"]:
												optionItem = meal( op )
												foodItem.addOption(title, optionItem, flex)
							base.append(foodItem)
			choices_outer.append([choices, addons])
	meals = []
	spent = 0
	score = 0
	while score < random.random():
		rest_index = random.randrange(len(choices_outer))
		rest_pick = choices_outer[rest_index]
		if len(rest_pick[0]) != 0:
			meal_index = random.randrange(len(rest_pick[0]))
			meal_pick = rest_pick[0][meal_index]
			final_meal, total_price = meal_pick.pickOptions(price)
			if total_price <= price - spent:
				meals.append(final_meal.toDict())
				spent = spent + total_price
			elif spent < total_price:
				meals = final_meal.toDict()
				spent = total_price
			score = (float(spent)/price)**2 + score
		else:
			score = score - 0.01
				# print "swap"
	return json.dumps({"core":meals, "total": spent })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

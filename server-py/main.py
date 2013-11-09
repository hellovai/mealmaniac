import api
import json
from datetime import timedelta
from flask import Flask, make_response, request, current_app
from functools import update_wrapper
import random

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
		self.price = item["price"]
		self.desc = item["descrip"]
		self.options = {}

	def toDict(self):
		return {
			"id":self.id,
			"name":self.name,
			"price":self.price,
			"desc":self.desc,
			"options":self.options
		}

	def addOption(self, key, option, choice=True):
		if key not in self.options:
			self.options[key] = {"flexible":choice, "data":[]}
		self.options[key]["data"].append(option)
		
@crossdomain(origin='*')
@app.route('/')
def hello_world():
    return 'Hoes better download the app'

@crossdomain(origin='*')
@app.route('/login/<email>/<pwd>')
def login(email, pwd):
	user = api.getUser(email)
	return json.dumps(user)

@crossdomain(origin='*')
@app.route('/meal/<uid>/<price>/<nick>')
def getMeal(uid, price, nick):
	user = api.getUser(uid)
	nearby = api.search(nick)
	price = int(10000 * float(price) / (100 + float(user["tip"]))) / 100.0
	print price
	# return json.dumps(nearby)
	choices = []
	for rest in nearby:
		if rest["mino"] <= price and rest["is_delivering"] == 1:
			rest_data = api.getDetails(rest["id"])
			if api.cuisineCheck(rest_data["cuisine"], uid):
				for category in rest_data["menu"]:
					for listing in category["children"]:
						if float(listing["price"]) < price:
							foodItem = meal(listing)
							if "children" in listing:
								for option in listing["children"]:
									if api.valid(option):
										title = option["name"]
										flex = api.checkFlexibility(title)
										if "children" in option:
											for op in option["children"]:
												optionItem = meal( op )
												foodItem.addOption(title, optionItem.toDict(), flex)
							choices.append(foodItem.toDict())
	random_index = random.randrange(len(choices))
	return json.dumps(choices[random_index])

if __name__ == '__main__':
    app.run(debug=True)
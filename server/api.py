base_url = "https://services-staging.grubhub.com/"
api_key = "SECRET"
format = "xml"

def constructURL(call, additions):
	res = base_url + call + "?"
	for key in additions:
		if additions[key] != None:
			res = res + "&" + key + "=" + additions[key]
	return res + "&format=" + format + "&apiKey=" + api_key

def fill(base, additions):
	for key in additions:
		if key in base:
			base[key] = additions[key]

def search(data):
	call = "services/search/results"
	fields = {
		"lat":None,
		"lng":None,
		"zipCode":None,
		"searchTerm":None,
		"restaurantType":None,
		"pickupRadius":None
	}
	fill(fields, data)
	url = constructURL(call, fields)
	return url

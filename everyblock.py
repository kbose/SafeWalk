import requests, pickle, json, datetime, re,time 

#if you need it fast 
from geopy.geocoders import GoogleV3 
geolocator = GoogleV3('GOOGLE_MAPS_API_KEY')

# from geopy.geocoders import Nominatim
# geolocator = Nominatim()

def get_nearby_crime_areas(city, zipcode):
	short_name_to_big_name = { "philly": "Philadelphia, PA", "boston": "Boston, MA", "chicago": "Chicago, IL",
			"houston": "Houstin, TX", "denver": "Denver, CO"}
	API_KEY = 'Token EVERYBLOCK_API_KEY'
	url = 'https://api.everyblock.com/content/%s/locations/%d/timeline/?schema=crime' %(city, zipcode)
	threshold_date_to_look = datetime.datetime.today() - datetime.timedelta(days=5) #days to look back
	h = { 'Authorization': API_KEY}
	r = requests.get(url,headers = h)
	
	#clean the request for info we want 
	def map_function(x):
		if datetime.datetime.strptime(x['item_date'],'%Y-%m-%d') >= threshold_date_to_look:
			return x['location_name']
		else:
			return 'NA'
	results = r.json()['results']
	location_names = filter(lambda x: x != "NA", map(map_function, results))
	i = 1
	while r.json()['next'] != None:
		i = i+1
		url = 'https://api.everyblock.com/content/philly/locations/19104/timeline/?page='+str(i)+'&schema=crime'
		r = requests.get(url,headers = h)
		results = r.json()['results']
		location_names.extend(filter(lambda x: x != "NA", map(map_function, results)))

	print location_names

	#clean the location names
	long_city_name = short_name_to_big_name[city]
	points_to_avoid = filter(lambda x: x != [],location_names)
	points_to_avoid_full_address = map(lambda x: (x + " " + long_city_name + " " + str(zipcode)).
		replace("Block ", "").encode("ascii"), points_to_avoid)
	
	def map_func(x):
		address_parts = x.split(" ")
		for i in range(len(address_parts)):
			if i != 0 and i != len(address_parts) - 1:
				all_num = re.compile("\d+")
				if all_num.match(address_parts[i]):
					address_parts[i] = ""
		address_parts = " ".join(address_parts)
		location = geolocator.geocode(address_parts, timeout = 15)
		if location != None:
			return (location.latitude,location.longitude)


	points_to_avoid_geoloc = filter(lambda x: x != None, map(map_func, points_to_avoid_full_address))
	return points_to_avoid_geoloc






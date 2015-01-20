from geopy.geocoders import Nominatim

geolocator = Nominatim()

def get_direction_points(directions):
	route = directions[0]["legs"][0]["steps"]
	start_location = None 
	try:
		start_location =  (float(route[0]['start_location']['lat']),float(route[1]['start_location']['lng']))
	except IndexError:
		start_location = None 

	route_points = map(lambda x: (float(x['end_location']['lat']), float(x['end_location']['lng'])), route)
	if start_location != None:
		return [start_location] + route_points
	else:
		return route_points


import csv, re 
zip_dict = {}
reader = csv.reader(open("zip_codes_ups.csv","rb"))
reader.next()
for row in reader:
	zip_dict[int(row[0])] = row[2]


def get_all_zipcodes(route_points):
	zipcodes = []
	short_name_to_big_name = {
	"philly": "Philadelphia, PA",
	"boston": "Boston, MA",
	"chicago": "Chicago, IL",
	"houston": "Houstin, TX",
	"denver": "Denver, CO"
	}
	for route_point in route_points:
		address, (latitude, longitude) = geolocator.reverse(route_point, timeout = 15 )

		spaces = address.replace(",","").split(" ")
		zipcode = None
		for i in spaces:
			all_chars_num = True
			for char in i:
				if char not in "0123456789":
					all_chars_num = False
			if all_chars_num:
				zipcode = int(i)

		if zipcode != None:	
			city = zip_dict[zipcode]

			for key in short_name_to_big_name:
				if city in short_name_to_big_name[key]:
					if {"short_name":key,"zipcode": zipcode} not in zipcodes:
						zipcodes.append({"short_name":key,"zipcode": zipcode})
	return zipcodes




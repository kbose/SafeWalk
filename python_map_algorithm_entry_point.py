import geopy, googlemaps, cPickle, datetime, re, sys, os 
from geopy.geocoders import Nominatim
import everyblock, way_points_calculate
import route_utils
import time 

gmaps = googlemaps.Client(key='GOOGLE_MAPS_API_KEY')
from geopy.geocoders import Nominatim
geolocator = Nominatim()

def map_entry(from_address, to_address):
	
	#google map request
	directions = gmaps.directions(from_address, to_address, mode="walking")

	#directions = cPickle.load(open("old_code/directions picke.pkl","rb"))
	route_points = route_utils.get_direction_points(directions) #longitude and latitude for points

	all_zones_to_look = route_utils.get_all_zipcodes(route_points)  #a json of all the necessary {"small_name", "zipcodes" we need for e}

	#make the request to the everyblock API for all the points_to_avoid
	points_to_avoid = [] 
	for zone in all_zones_to_look:
		points_to_avoid.extend(everyblock.get_nearby_crime_areas(zone["short_name"], zone["zipcode"]))
	
	print points_to_avoid, all_zones_to_look

	#compute the waypoints to long/lat 
	way_points = way_points_calculate.get_way_points(points_to_avoid, route_points)
	way_points = list(set(way_points))

	print  way_points

	#compute the addresses 
	# def map_function(x):
	# 	address, (latitude, longitude) = geolocator.reverse(x, timeout = 15)
	# 	return address
	# text_way_points = map(map_function,way_points)
	# text_way_points = list(set(text_way_points))
	if len(way_points) > 8:
		return "NOT PROCESSABLE" #just display the default
	else:
		return "|".join(map(lambda x: str(x),way_points))


wp = map_entry("3400 Spruce Street, Philadelphia, PA 19104","202 South 37th Street, Philadelphia, PA 19104")
print wp





	
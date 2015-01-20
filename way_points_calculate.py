import geopy, googlemaps, cPickle, datetime, math 

import everyblock

distance_limit = 0.001 #about 0.1 miles, one block, good distance to keep 

#distance in longitude and latitude units
def distance(point_A, point_B):
	sqrt_val = math.sqrt(((point_A[0] - point_B[0])**2 + (point_A[1] - point_B[1])**2))
	return sqrt_val

#returns the list of points that are surround  
def get_radially_away(point, degree_increment, radius):
	points_to_return = []
	degree_searched = 0
	while degree_searched < 361:
		new_point_long = point[1] + math.cos(math.radians(degree_searched))*radius
		new_point_lat = point[0] + math.sin(math.radians(degree_searched))*radius
		degree_searched += degree_increment
		points_to_return.append((new_point_lat, new_point_long))
	return points_to_return


def get_way_points(points_to_avoid, route_points):
	way_points = []
	for i in range(len(route_points)):
		route_point = route_points[i]
		best_waypoint = None 
		for avoid_point in points_to_avoid:
			if distance(avoid_point, route_point) < distance_limit:
				possible_alternatives  = get_radially_away(route_point, 60, distance_limit)
				for alt in possible_alternatives:
					if distance(alt, avoid_point) > distance_limit:
						if best_waypoint == None:
							best_waypoint = alt 
						elif distance(alt,route_points[i]) < distance(best_waypoint,route_points[i]):
							best_waypoint = alt
		if best_waypoint != None: #all are too close, just give none 
			not_close_to_existing = True 
			for existing_way_point in way_points:
				if distance(best_waypoint, existing_way_point) < distance_limit:
					not_close_to_existing = False
			if not_close_to_existing:
				way_points.append(best_waypoint)

	#filter the way points based on whether they are closer to the start or not 
	start_loc = route_points[0]
	end_loc = route_points[-1] 
	way_points = filter(lambda x: distance(x, end_loc) < distance(start_loc,end_loc), way_points) 
	return way_points


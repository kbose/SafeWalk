#!/usr/bin/env python2

from flask import * 
app = Flask(__name__)
from python_map_algorithm_entry_point import *

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit(back=None): 
    if request.method == 'POST':
        loc1 = request.form['origin']
        loc2 = request.form['destination']
        ret = map_entry(loc1, loc2)
	if ret == 'NOT PROCESSABLE':
            uri = ('https://www.google.com/maps/embed/v1/directions?key=GOOGLE_MAPS_EMBED_API-LU&mode=walking&origin=' + loc1 + '&destination=' + loc2)
            uri = uri.replace(" ","+")
        elif len(ret) > 0 :
            uri = ('https://www.google.com/maps/embed/v1/directions?key=GOOGLE_MAPS_EMBED_API-LU&mode=walking&origin=' + loc1 + '&destination=' + loc2 + '&waypoints=' + ret)
	    uri = uri.replace(" ","+")
	else :
	    uri = ('https://www.google.com/maps/embed/v1/directions?key=GOOGLE_MAPS_EMBED_API-LU&mode=walking&origin=' + loc1 + '&destination=' + loc2)
	    uri = uri.replace(" ","+")
	return render_template('index.html', back=uri)
    else:
        return None     

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


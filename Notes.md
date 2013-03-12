# TODO

* Wait for Dimi/Wouter remarks 
* (Relire mockup)
* Compare data to real atlas
* Fabric script
* Imagine UI withh full-size / background map
* Better color picker: show color, ...
* Complex style when multiple searches on one square
* BUG: !! Some squares are outside of Belgium (but close!)...

# How to edit Bootstrap theme (changing colors, ...)

0. Requirements to compile Bootstrap: Node.js (with npm tool), then do $ npm install -g less jshint recess uglify-js
1. Go to bootstrap-2.2.2 directory (Bootstrap sources)
2. Change what you want (mainly in less/variables.less)
3. $ make bootstrap (do $make clean before if bootstrap directory already exists), a bootstrap directory is generated
4. Copy generated files in ./bootstrap to Django "static" folder

# Postgresl Notes:

* createdb -U postgres -h localhost -p 5432 formidabel


# API:
http://localhost:8000/en/api/v1/genus/3/?format=json => 

/en/api/v1/occurrence/?event_date__gte=2012-08-10&format=json

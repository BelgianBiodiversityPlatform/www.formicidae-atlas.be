# TODO


* Make website lmayout (wait for content?)
* Wait for Dimi/Wouter remarks 
* Compare data to real atlas
* Fabric script
* Imagine UI withh full-size / background map
* Better color picker: show color, ...
* BUG: !! Some squares are outside of Belgium (but close!)...
* Make date format consitent (search form / layer list, ... )

# How to edit Bootstrap theme (changing colors, ...)

0. Requirements to compile Bootstrap: Node.js (with npm tool), then do $ npm install -g less jshint recess uglify-js (on dev. machine, just make sure /usr/local/share/npm/bin is in PATH)
1. Go to bootstrap-2.2.2 directory (Bootstrap sources)
2. Change what you want (mainly in less/variables.less)
3. $ make clean && make bootstrap, a bootstrap directory is generated
4. Copy generated files in ./bootstrap to Django "static" folder:
cp -R bootstrap/* ../formidabel/static/

# Postgresl Notes:

* createdb -U postgres -h localhost -p 5432 formidabel


# API:
http://localhost:8000/en/api/v1/genus/3/?format=json => 

/en/api/v1/occurrence/?event_date__gte=2012-08-10&format=json

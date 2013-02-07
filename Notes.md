# TODO

# How to edit Bootstrap theme (changing colors, ...)

0. Requirements to compile Bootstrap: Node.js (with npm tool), then do $ npm install -g less jshint recess uglify-js
1. Go to bootstrap-2.2.2 directory (Bootstrap sources)
2. Change what you want (mainly in less/variables.less)
3. $ make bootstrap (do $make clean before if bootstrap directory already exists), a bootstrap directory is generated
4. Copy generated files in ./bootstrap to Django "static" folder
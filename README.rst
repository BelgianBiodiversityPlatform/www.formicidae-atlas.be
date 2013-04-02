Architecture overview
=====================

This is a Django project made of two main apps:

- A `django CMS`_ install to manage simple content (static texts, images, ...)
- A custom 'formidabel' Django app that allows searching and displaying ants occurrences on a `Leaflet`_ map. It imports its data directly from the Darwin Core Archive published by the `IPT`_.

Deployment instructions
=======================

(TODO: improve this)

- Install requirements
- Create localsettings.py
- Create database (and configure it with dj-database-url)
- Create an admin and basic CMS pages
- Configure the formidabel AppHook on a page
- Import DwcA data into formidabel

Visual customization
====================

App-specific CSS can be edited in formidabel/static/css/formidabel.css.

The design is based on `Bootstrap`_. It is therefore possible to recompile Bootstrap with different options to make it looks more custom:

0. Node.js is a requirement. NPM can then be used to install other Bootstrap dependencies:
    
    ::

        $ npm install -g less jshint recess uglify-js          


1. Go to Bootstrap sources

    ::

        $ cd bootstrap-2.2.2

2. Edit files (mainly in less/variables.less)
3. Compile Bootstrap:

    ::

        $ make clean && make bootstrap # A bootstrap directory is generated

4. Copy resulting files in in static assets of the app: 

    ::

        $ cp -R bootstrap/* ../formidabel/static/

.. _django CMS: https://www.django-cms.org/en/
.. _Leaflet: http://leafletjs.com/
.. _IPT: https://code.google.com/p/gbif-providertoolkit/
.. _Bootstrap: http://twitter.github.com/bootstrap/


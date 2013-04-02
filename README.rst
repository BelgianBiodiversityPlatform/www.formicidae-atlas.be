Architecture overview
=====================

This is a Django project made of two main apps:

- A `django CMS`_ install to manage simple content (static texts, images, ...)
- A custom 'formidabel' Django app that allows searching and displaying ants occurrences on a `Leaflet`_ map. It imports its data directly from the Darwin Core Archive published by the `IPT`_.

Deployment instructions
=======================

(TODO: improve this)

- Install requirements
- Create an admin and basic CMS pages
- Configure the formidabel AppHook on a page
- Import DwcA data into formidabel

.. _django CMS: https://www.django-cms.org/en/
.. _Leaflet: http://leafletjs.com/
.. _IPT: https://code.google.com/p/gbif-providertoolkit/
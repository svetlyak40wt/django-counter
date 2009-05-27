Introduction
============

This is a general purpose page views / redirects counter for django projects.

Dependencies
------------

This application depends on PIL_.

Installation
------------

* Add application ``django_counter`` to the ``INSTALLED_APPS`` list.
* Run ``./manage.py syncdb`` to create all neccessary tables.

Usage
-----

View counter
^^^^^^^^^^^^

View counter is linked to particular object.
First, you need to add and `img` element on the page with object:

    {% load counter_tags %}
    {% counter object %}

The second line add an invisible image on the page. When browser gets this image, counter is incremented.

Next, you if you need to output a total number of page views somewhere, add these lines in your template:

    {% load counter_tags %}
    {% view_count for blog.entry object.id as page_views %}
    <p>Object viewed: {{ page_views }} times.</p>

Redirects counter
^^^^^^^^^^^^^^^^^

To use redirect counter, create one through admin interface and put anywhere link to a redirector. It can look
like http://example.com/counter/r/123/.

After that, you can collect redirects and referers statistic in the admin interface.

Contacts
--------

Author: Alexander Artemenko

Please send any suggesions and patches to svetlyak.40wt at google mail, or to
http://github.com/svetlyak40wt/django-counter/

.. _django: http://djangoproject.org
.. _PIL: http://www.pythonware.com/products/pil/


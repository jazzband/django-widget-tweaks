====================
django-widget-tweaks
====================

Tweak the form field rendering in templates, not in python-level
form definitions. Altering CSS classes and HTML attributes is supported.

That should be enough for designers to customize field presentation (using
CSS and unobtrusive javascript) without touching python code.

The license is MIT.

Installation
============

::

    pip install django-widget-tweaks

Then add 'widget_tweaks' to INSTALLED_APPS.

Usage
=====

This app provides several template filters that can alter CSS classes and
HTML attributes of django form fields.

attr
----
Adds or replaces any single html atribute for the form field.

Examples::

    {% load widget_tweaks %}

    <!-- change input type (e.g. to HTML5) -->
    {{ form.search_query|attr:"type:search" }}

    <!-- add/change several attributes -->
    {{ form.text|attr:"rows:20"|attr:"cols:20"|attr:"title:Hello, world!" }}

    <!-- attributes without parameters -->
    {{ form.search_query|attr:"autofocus" }}


add_class
---------

Adds CSS class to field element. Split classes by whitespace in order to add
several classes at once.

Example::

    {% load widget_tweaks %}

    <!-- add 2 extra css classes to field element -->
    {{ form.title|add_class:"css_class_1 css_class_2" }}

set_data
--------

Sets HTML5 data attribute ( http://ejohn.org/blog/html-5-data-attributes/ ).
Useful for unobtrusive javascript. It is just a shortcut for 'attr' filter
that prepends attribute names with 'data-' string.

Example::

    {% load widget_tweaks %}

    <!-- data-filters:"OverText" will be added to input field -->
    {{ form.title|set_data:"filters:OverText" }}

append_attr
-----------

Appends atribute value with extra data.

Example::

    {% load widget_tweaks %}

    <!-- add 2 extra css classes to field element -->
    {{ form.title|append_attr:"class:css_class_1 css_class_2" }}

'add_class' filter is just a shortcut for 'append_attr' filter that
adds values to the 'class' attribute.

add_error_class
---------------

The same as 'add_class' but adds css class only if validation failed for
the field (field.errors is not empty).

Example::

    {% load widget_tweaks %}

    <!-- add 'error-border' css class on field error -->
    {{ form.title|add_error_class:"error-border" }}

render_field
------------

This is a template tag that can be used as an alternative to aforementioned
filters.  This template tag renders a field using a syntax similar to plain
HTML attributes.

Example::

    {% load widget_tweaks %}

    <!-- change input type (e.g. to HTML5) -->
    {% render_field form.search_query type="search" %}

    <!-- add/change several attributes -->
    {% render_field form.text rows="20" cols="20" title="Hello, world!" %}
    
    <!-- add/change several attributes with use template variable -->
    {% render_field form.text placeholder=form.text.label %}

    <!-- append to an attribute -->
    {% render_field form.title class+="css_class_1 css_class_2" %}

field_type widget_type
----------------------

Tags for get field class name and field widget class name in lower case.

Example::

    <div class="field {{ field|field_type }} {{ field|widget_type }}
                {{ field.html_name }}">
        {{ field }}
    </div>
    
    Out:
    
    <div class="field charfield textinput 
                name">
        <input id="id_name" type="text" name="name" maxlength="100" />
    </div>

 
Contributing
============

If you've found a bug, implemented a feature or have a suggestion,
do not hesitate to contact me, fire an issue or send a pull request.

Source code:

* https://bitbucket.org/kmike/django-widget-tweaks/
* https://github.com/kmike/django-widget-tweaks/

Bug tracker: https://bitbucket.org/kmike/django-widget-tweaks/issues/new

running the tests
-----------------

Make sure you have `tox <http://tox.testrun.org/>`_ installed, then type

::

    tox

from the source checkout.

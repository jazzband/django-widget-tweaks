====================
django-widget-tweaks
====================

.. image:: https://travis-ci.org/kmike/django-widget-tweaks.png?branch=master
    :target: https://travis-ci.org/kmike/django-widget-tweaks
.. image:: https://coveralls.io/repos/kmike/django-widget-tweaks/badge.png?branch=master
    :target: https://coveralls.io/r/kmike/django-widget-tweaks

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


add_error_attr
--------------

The same as 'attr' but sets an attribute only if validation failed for
the field (field.errors is not empty). This can be useful when dealing
with accessibility::

    {% load widget_tweaks %}

    <!-- add aria-invalid="true" attribute on field error -->
    {{ form.title|add_error_attr:"aria-invalid:true" }}



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

    <!-- append to an attribute -->
    {% render_field form.title class+="css_class_1 css_class_2" %}

    <!-- template variables can be used as attribute values -->
    {% render_field form.text placeholder=form.text.label %}

For fields rendered with ``{% render_field %}`` tag it is possible
to set error class and required fields class by using
``WIDGET_ERROR_CLASS`` and  ``WIDGET_REQUIRED_CLASS`` template variables::

    {% with WIDGET_ERROR_CLASS='my_error' WIDGET_REQUIRED_CLASS='my_required' %}
        {% render_field form.field1 %}
        {% render_field form.field2 %}
        {% render_field form.field3 %}
    {% endwith %}

You can be creative with these variables: e.g. a context processor could
set a default CSS error class on all fields rendered by
``{% render_field %}``.

field_type and widget_type
--------------------------

``'field_type'`` and ``'widget_type'`` are template filters that return
field class name and field widget class name (in lower case).

Example::

    {% load widget_tweaks %}

    <div class="field {{ field|field_type }} {{ field|widget_type }} {{ field.html_name }}">
        {{ field }}
    </div>

Output::

    <div class="field charfield textinput name">
        <input id="id_name" type="text" name="name" maxlength="100" />
    </div>

Filter chaining
===============

The order django-widget-tweaks filters apply may seem counter-intuitive
(leftmost filter wins)::

    {{ form.simple|attr:"foo:bar"|attr:"foo:baz" }}

returns::

    <input foo="bar" type="text" name="simple" id="id_simple" />

It is not a bug, it is a feature that enables creating reusable templates
with overridable defaults.

Reusable field template example::

    {# inc/field.html #}
    {% load widget_tweaks %}
    <div>{{ field|attr:"foo:default_foo" }}</div>

Example usage::

    {# my_template.html #}
    {% load widget_tweaks %}
    <form method='POST' action=''> {% csrf_token %}
        {% include "inc/field.html" with field=form.title %}
        {% include "inc/field.html" with field=form.description|attr:"foo:non_default_foo" %}
    </form>

With 'rightmost filter wins' rule it wouldn't be possible to override
``|attr:"foo:default_foo"`` in main template.

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

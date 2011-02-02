#!/usr/bin/env python
from distutils.core import setup
version='0.2'

setup(
    name = 'django-widget-tweaks',
    version = version,
    author = 'Mikhail Korobov',
    author_email = 'kmike84@gmail.com',
    url = 'http://bitbucket.org/kmike/django-widget-tweaks/',
    download_url = 'http://bitbucket.org/kmike/django-widget-tweaks/get/tip.zip',

    description = 'Tweak the form field rendering in templates, not in python-level form definitions.',
    long_description = open('README.rst').read(),
    license = 'MIT license',
    requires = ['django'],

    packages=['widget_tweaks', 'widget_tweaks.templatetags'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)

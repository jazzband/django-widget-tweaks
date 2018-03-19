#!/usr/bin/env python
from setuptools import setup

version = '1.4.2'

setup(
    name='django-widget-tweaks',
    version=version,
    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',
    url='https://github.com/jazzband/django-widget-tweaks',
    description='Tweak the form field rendering in templates, not in python-level form definitions.',
    long_description=open('README.rst').read() + "\n\n" + open('CHANGES.rst').read(),
    license='MIT license',
    requires=['django (>= 1.8)'],
    packages=['widget_tweaks', 'widget_tweaks.templatetags'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)

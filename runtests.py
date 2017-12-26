#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import django
from django.conf import settings
from django.core.management import call_command

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

opts = {'INSTALLED_APPS': ['widget_tweaks']}

if django.VERSION[:2] < (1, 5):
    opts['DATABASES'] = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':MEMORY:',
        }
    }

if django.VERSION[:2] >= (1, 10):
    opts['TEMPLATES'] = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
        },
    ]

settings.configure(**opts)

if django.VERSION[:2] >= (1, 7):
    django.setup()

if __name__ == "__main__":
    call_command('test', 'widget_tweaks', verbosity=2)

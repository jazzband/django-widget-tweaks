#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import django
from django.conf import settings
from django.core.management import call_command

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

settings.configure(
    INSTALLED_APPS=('widget_tweaks',),
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':MEMORY:',
        }
    }
)
if django.VERSION[:2] >= (1, 7):
    django.setup()

if __name__ == "__main__":
    call_command('test', 'widget_tweaks')
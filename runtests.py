#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import django
from django.conf import settings
from django.core.management import call_command

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

opts = {'INSTALLED_APPS': ['widget_tweaks']}

if django.VERSION[:2] >= (1, 10):
    opts['TEMPLATES'] = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
        },
    ]

settings.configure(**opts)
django.setup()

if __name__ == "__main__":
    param = "" if not len(sys.argv) >= 2  else "." +str(sys.argv[1])
    call_command('test', 'widget_tweaks{}'.format(param), verbosity=2)

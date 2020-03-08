#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import django
from django.conf import settings
from django.core.management import call_command

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

opts = {"INSTALLED_APPS": ["widget_tweaks"]}

if django.VERSION[:2] >= (1, 10):
    opts["TEMPLATES"] = [
        {"BACKEND": "django.template.backends.django.DjangoTemplates",},
    ]

settings.configure(**opts)
django.setup()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Allow running specific tests with arguments e.g.
        # tox -e py36-django-20 -- tests.RenderFieldTagFieldReuseTest.test_field_datetime_widget
        test_name = sys.argv[1]
        call_command(
            "test", "widget_tweaks.{test_name}".format(test_name=test_name), verbosity=2
        )
    else:
        call_command("test", "widget_tweaks", verbosity=2)

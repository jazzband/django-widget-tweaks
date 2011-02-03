from django.test import TestCase
from django.forms import Form, CharField, TextInput
from django import forms
from django.template import Template, Context

class MyForm(Form):
    simple = CharField()
    with_attrs = CharField(widget=TextInput(attrs={
                    'foo':'baz',
                    'egg': 'spam'
                 }))
    with_cls = CharField(widget=TextInput(attrs={'class':'class0'}))

def render_field(field, filter, params, *args):
    filters = [(filter, params)]
    filters.extend(zip(args[::2], args[1::2]))
    filter_strings = ['|%s:"%s"' % (f[0], f[1],) for f in filters]
    render_field_str = '{{ form.%s%s }}' % (field, ''.join(filter_strings))

    tpl = Template("{% load widget_tweaks %}" + render_field_str)
    context = Context({'form': MyForm()})
    return tpl.render(context)

def assertIn(value, obj):
    assert value in obj, "%s not in %s" % (value, obj,)

def assertNotIn(value, obj):
    assert value not in obj, "%s in %s" % (value, obj,)

class SimpleAttrTest(TestCase):
    def test_attr(self):
        res = render_field('simple', 'attr', 'foo:bar')
        assertIn('type="text"', res)
        assertIn('name="simple"', res)
        assertIn('id="id_simple"', res)
        assertIn('foo="bar"', res)

    def test_attr_chaining(self):
        res = render_field('simple', 'attr', 'foo:bar', 'attr', 'bar:baz')
        assertIn('type="text"', res)
        assertIn('name="simple"', res)
        assertIn('id="id_simple"', res)
        assertIn('foo="bar"', res)
        assertIn('bar="baz"', res)

    def test_add_class(self):
        res = render_field('simple', 'add_class', 'foo')
        assertIn('class="foo"', res)

    def test_add_multiple_classes(self):
        res = render_field('simple', 'add_class', 'foo bar')
        assertIn('class="foo bar"', res)

    def test_add_class_chaining(self):
        res = render_field('simple', 'add_class', 'foo', 'add_class', 'bar')
        assertIn('class="bar foo"', res)

class CustomizedWidgetTest(TestCase):
    def test_attr(self):
        res = render_field('with_attrs', 'attr', 'foo:bar')
        assertIn('foo="bar"', res)
        assertNotIn('foo="baz"', res)
        assertIn('egg="spam"', res)

    def test_attr_chaining(self):
        res = render_field('with_attrs', 'attr', 'foo:bar', 'attr', 'bar:baz')
        assertIn('foo="bar"', res)
        assertNotIn('foo="baz"', res)
        assertIn('egg="spam"', res)
        assertIn('bar="baz"', res)

    def test_attr_class(self):
        res = render_field('with_cls', 'attr', 'foo:bar')
        assertIn('foo="bar"', res)
        assertIn('class="class0"', res)

    def test_default_attr(self):
        res = render_field('with_cls', 'attr', 'type:search')
        assertIn('class="class0"', res)
        assertIn('type="search"', res)

    def test_add_class(self):
        res = render_field('with_cls', 'add_class', 'class1')
        assertIn('class0', res)
        assertIn('class1', res)

    def test_add_class_chaining(self):
        res = render_field('with_cls', 'add_class', 'class1', 'add_class', 'class2')
        assertIn('class0', res)
        assertIn('class1', res)
        assertIn('class2', res)

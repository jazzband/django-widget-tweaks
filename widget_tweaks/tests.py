import string
try:
    from django.utils.unittest import expectedFailure
except ImportError:
    def expectedFailure(func):
        return lambda *args, **kwargs: None

from django.test import TestCase
from django.forms import Form, CharField, TextInput
from django import forms
from django.template import Template, Context
from django.forms.extras.widgets import SelectDateWidget


class MyForm(Form):
    simple = CharField()
    with_attrs = CharField(widget=TextInput(attrs={
                    'foo':'baz',
                    'egg': 'spam'
                 }))
    with_cls = CharField(widget=TextInput(attrs={'class':'class0'}))
    date = forms.DateField(widget=SelectDateWidget(attrs={'egg': 'spam'}))

def render_form(text):
    tpl = Template("{% load widget_tweaks %}" + text)
    context = Context({'form': MyForm()})
    return tpl.render(context)


def render_field(field, filter, params, *args):
    filters = [(filter, params)]
    filters.extend(zip(args[::2], args[1::2]))
    filter_strings = ['|%s:"%s"' % (f[0], f[1],) for f in filters]
    render_field_str = '{{ form.%s%s }}' % (field, ''.join(filter_strings))
    return render_form(render_field_str)

def render_field_from_tag(field, *attributes):
    attr_strings = [' %s' % f for f in attributes]
    tpl = string.Template('{% render_field form.$field$attrs %}')
    render_field_str = tpl.substitute(field=field, attrs=''.join(attr_strings))
    return render_form(render_field_str)

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

class SilenceTest(TestCase):
    def test_silence_without_field(self):
        res = render_field("nothing", 'attr', 'foo:bar')
        self.assertEquals(res, "")
        res = render_field("nothing", 'add_class', 'some')
        self.assertEquals(res, "")

class CustomizedWidgetTest(TestCase):
    def test_attr(self):
        res = render_field('with_attrs', 'attr', 'foo:bar')
        assertIn('foo="bar"', res)
        assertNotIn('foo="baz"', res)
        assertIn('egg="spam"', res)

    # see https://code.djangoproject.com/ticket/16754
    @expectedFailure
    def test_selectdatewidget(self):
        res = render_field('date', 'attr', 'foo:bar')
        assertIn('egg="spam"', res)
        assertIn('foo="bar"', res)

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


class FieldReuseTest(TestCase):

    def test_field_double_rendering_simple(self):
        res = render_form('{{ form.simple }}{{ form.simple|attr:"foo:bar" }}{{ form.simple }}')
        self.assertEqual(res.count("bar"), 1)

    def test_field_double_rendering_simple_css(self):
        res = render_form('{{ form.simple }}{{ form.simple|add_class:"bar" }}{{ form.simple|add_class:"baz" }}')
        self.assertEqual(res.count("baz"), 1)
        self.assertEqual(res.count("bar"), 1)

    def test_field_double_rendering_attrs(self):
        res = render_form('{{ form.with_cls }}{{ form.with_cls|add_class:"bar" }}{{ form.with_cls }}')
        self.assertEqual(res.count("class0"), 3)
        self.assertEqual(res.count("bar"), 1)


class SimpleRenderFieldTagTest(TestCase):
    def test_attr(self):
        res = render_field_from_tag('simple', 'foo="bar"')
        assertIn('type="text"', res)
        assertIn('name="simple"', res)
        assertIn('id="id_simple"', res)
        assertIn('foo="bar"', res)

    def test_multiple_attrs(self):
        res = render_field_from_tag('simple', 'foo="bar"', 'bar="baz"')
        assertIn('type="text"', res)
        assertIn('name="simple"', res)
        assertIn('id="id_simple"', res)
        assertIn('foo="bar"', res)
        assertIn('bar="baz"', res)


class RenderFieldTagSilenceTest(TestCase):
    def test_silence_without_field(self):
        res = render_field_from_tag("nothing", 'foo="bar"')
        self.assertEquals(res, "")
        res = render_field_from_tag("nothing", 'class+="some"')
        self.assertEquals(res, "")


class RenderFieldTagCustomizedWidgetTest(TestCase):
    def test_attr(self):
        res = render_field_from_tag('with_attrs', 'foo="bar"')
        assertIn('foo="bar"', res)
        assertNotIn('foo="baz"', res)
        assertIn('egg="spam"', res)

    # see https://code.djangoproject.com/ticket/16754
    @expectedFailure
    def test_selectdatewidget(self):
        res = render_field_from_tag('date', 'foo="bar"')
        assertIn('egg="spam"', res)
        assertIn('foo="bar"', res)

    def test_multiple_attrs(self):
        res = render_field_from_tag('with_attrs', 'foo="bar"', 'bar="baz"')
        assertIn('foo="bar"', res)
        assertNotIn('foo="baz"', res)
        assertIn('egg="spam"', res)
        assertIn('bar="baz"', res)

    def test_attr_class(self):
        res = render_field_from_tag('with_cls', 'foo="bar"')
        assertIn('foo="bar"', res)
        assertIn('class="class0"', res)

    def test_default_attr(self):
        res = render_field_from_tag('with_cls', 'type="search"')
        assertIn('class="class0"', res)
        assertIn('type="search"', res)

    def test_append_attr(self):
        res = render_field_from_tag('with_cls', 'class+="class1"')
        assertIn('class0', res)
        assertIn('class1', res)

    def test_duplicate_append_attr(self):
        res = render_field_from_tag('with_cls', 'class+="class1"', 'class+="class2"')
        assertIn('class0', res)
        assertIn('class1', res)
        assertIn('class2', res)

    def test_hyphenated_attributes(self):
        res = render_field_from_tag('with_cls', 'data-foo="bar"')
        assertIn('data-foo="bar"', res)
        assertIn('class="class0"', res)


class RenderFieldTagFieldReuseTest(TestCase):
    def test_field_double_rendering_simple(self):
        res = render_form('{{ form.simple }}{% render_field form.simple foo="bar" %}{% render_field form.simple %}')
        self.assertEqual(res.count("bar"), 1)

    def test_field_double_rendering_simple_css(self):
        res = render_form('{% render_field form.simple %}{% render_field form.simple class+="bar" %}{% render_field form.simple class+="baz" %}')
        self.assertEqual(res.count("baz"), 1)
        self.assertEqual(res.count("bar"), 1)

    def test_field_double_rendering_attrs(self):
        res = render_form('{% render_field form.with_cls %}{% render_field form.with_cls class+="bar" %}{% render_field form.with_cls %}')
        self.assertEqual(res.count("class0"), 3)
        self.assertEqual(res.count("bar"), 1)
        
class RenderFieldTagUseTemplateVariableTest(TestCase):
    def test_use_template_variable_in_parametrs(self):
        res = render_form('{% render_field form.with_attrs egg+="pahaz" placeholder=form.with_attrs.label %}')
        assertIn('egg="spam pahaz"', res)
        assertIn('placeholder="With attrs"', res)
        
class RenderFieldFilter_field_type_widget_type_Test(TestCase):
    def test_field_type_widget_type_rendering_simple(self):
        res = render_form('<div class="{{ form.simple|field_type }} {{ form.simple|widget_type }} {{ form.simple.html_name }}">{{ form.simple }}</div>')
        assertIn('class="charfield textinput simple"', res)

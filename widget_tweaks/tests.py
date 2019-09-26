import string

try:
    from unittest import TestCase, skipIf
except ImportError:
    from unittest2 import TestCase, skipIf

from django import VERSION
from django import forms
from django.forms import Form, CharField, TextInput
from django.template import Template, Context

try:
    from django.forms import SelectDateWidget  # django >= 2.0
except ImportError:
    from django.forms.extras.widgets import SelectDateWidget  # django < 2.0


# ==============================
#       Testing helpers
# ==============================

class MyForm(Form):
    """
    Test form. If you want to test rendering of a field,
    add it to this form and use one of 'render_...' functions
    from this module.
    """
    simple = CharField()
    with_attrs = CharField(widget=TextInput(attrs={
        'foo': 'baz',
        'egg': 'spam'
    }))
    with_cls = CharField(widget=TextInput(attrs={'class': 'class0'}))
    date = forms.DateField(widget=SelectDateWidget(attrs={'egg': 'spam'}))


def render_form(text, form=None, **context_args):
    """
    Renders template ``text`` with widget_tweaks library loaded
    and MyForm instance available in context as ``form``.
    """
    tpl = Template("{% load widget_tweaks %}" + text)
    context_args.update({'form': MyForm() if form is None else form})
    context = Context(context_args)
    return tpl.render(context)


def render_field(field, template_filter, params, *args, **kwargs):
    """
    Renders ``field`` of MyForm with filter ``template_filter`` applied.
    ``params`` are filter arguments.

    If you want to apply several filters (in a chain),
    pass extra ``template_filter`` and ``params`` as positional arguments.

    In order to use custom form, pass form instance as ``form``
    keyword argument.
    """
    filters = [(template_filter, params)]
    filters.extend(zip(args[::2], args[1::2]))
    filter_strings = ['|%s:"%s"' % (f[0], f[1],) for f in filters]
    render_field_str = '{{ form.%s%s }}' % (field, ''.join(filter_strings))
    return render_form(render_field_str, **kwargs)


def render_field_from_tag(field, *attributes):
    """
    Renders MyForm's field ``field`` with attributes passed
    as positional arguments.
    """
    attr_strings = [' %s' % f for f in attributes]
    tpl = string.Template('{% render_field form.$field$attrs %}')
    render_field_str = tpl.substitute(field=field, attrs=''.join(attr_strings))
    return render_form(render_field_str)


def assertIn(value, obj):
    assert value in obj, "%s not in %s" % (value, obj,)


def assertNotIn(value, obj):
    assert value not in obj, "%s in %s" % (value, obj,)


# ===============================
#           Test cases
# ===============================

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

    def test_set_data(self):
        res = render_field('simple', 'set_data', 'key:value')
        assertIn('data-key="value"', res)

    def test_replace_type(self):
        res = render_field('simple', 'attr', 'type:date')
        self.assertTrue(res.count("type=") == 1, (res, res.count("type=")))
        assertIn('type="date"', res)

    def test_replace_hidden(self):
        res = render_field('simple', 'attr', 'type:hidden')
        self.assertTrue(res.count("type=") == 1, (res, res.count("type=")))
        assertIn('type="hidden"', res)


class ErrorsTest(TestCase):

    def _err_form(self):
        form = MyForm({'foo': 'bar'})  # some random data
        form.is_valid()  # trigger form validation
        return form

    def test_error_class_no_error(self):
        res = render_field('simple', 'add_error_class', 'err')
        assertNotIn('class="err"', res)

    def test_error_class_error(self):
        form = self._err_form()
        res = render_field('simple', 'add_error_class', 'err', form=form)
        assertIn('class="err"', res)

    def test_error_attr_no_error(self):
        res = render_field('simple', 'add_error_attr', 'aria-invalid:true')
        assertNotIn('aria-invalid="true"', res)

    def test_error_attr_error(self):
        form = self._err_form()
        res = render_field('simple', 'add_error_attr', 'aria-invalid:true', form=form)
        assertIn('aria-invalid="true"', res)


class SilenceTest(TestCase):
    def test_silence_without_field(self):
        res = render_field("nothing", 'attr', 'foo:bar')
        self.assertEqual(res, "")
        res = render_field("nothing", 'add_class', 'some')
        self.assertEqual(res, "")
        res = render_field("nothing", 'remove_attr', 'some')
        self.assertEqual(res, "")


class CustomizedWidgetTest(TestCase):
    def test_attr(self):
        res = render_field('with_attrs', 'attr', 'foo:bar')
        assertIn('foo="bar"', res)
        assertNotIn('foo="baz"', res)
        assertIn('egg="spam"', res)

    # XXX can be dropped once 1.8 is not supported
    @skipIf(VERSION < (1, 11, 0, 'final', 0), 'see https://code.djangoproject.com/ticket/16754')
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

    def test_remove_attr(self):
        res = render_field('with_attrs', 'remove_attr', 'foo')
        assertNotIn('foo', res)


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
        self.assertEqual(res, "")
        res = render_field_from_tag("nothing", 'class+="some"')
        self.assertEqual(res, "")


class RenderFieldTagCustomizedWidgetTest(TestCase):
    def test_attr(self):
        res = render_field_from_tag('with_attrs', 'foo="bar"')
        assertIn('foo="bar"', res)
        assertNotIn('foo="baz"', res)
        assertIn('egg="spam"', res)

    # XXX can be dropped once 1.8 is not supported
    @skipIf(VERSION < (1, 11, 0, 'final', 0), 'see https://code.djangoproject.com/ticket/16754')
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


class RenderFieldWidgetClassesTest(TestCase):
    def test_use_widget_required_class(self):
        res = render_form('{% render_field form.simple %}',
                          WIDGET_REQUIRED_CLASS='required_class')
        assertIn('class="required_class"', res)

    def test_use_widget_error_class(self):
        res = render_form('{% render_field form.simple %}', form=MyForm({}),
                          WIDGET_ERROR_CLASS='error_class')
        assertIn('class="error_class"', res)

    def test_use_widget_error_class_with_other_classes(self):
        res = render_form('{% render_field form.simple class="blue" %}',
                          form=MyForm({}), WIDGET_ERROR_CLASS='error_class')
        assertIn('class="blue error_class"', res)

    def test_use_widget_required_class_with_other_classes(self):
        res = render_form('{% render_field form.simple class="blue" %}',
                          form=MyForm({}), WIDGET_REQUIRED_CLASS='required_class')
        assertIn('class="blue required_class"', res)


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

    def test_field_double_rendering_id(self):
        res = render_form(
            '{{ form.simple }}'
            '{% render_field form.simple id="id_1" %}'
            '{% render_field form.simple id="id_2" %}'
        )
        self.assertEqual(res.count("id_1"), 1)
        self.assertEqual(res.count("id_2"), 1)

    def test_field_double_rendering_id_name(self):
        res = render_form(
            '{{ form.simple }}'
            '{% render_field form.simple id="id_1" name="n_1" %}'
            '{% render_field form.simple id="id_2" name="n_2" %}'
        )
        self.assertEqual(res.count("id_1"), 1)
        self.assertEqual(res.count("id_2"), 1)
        self.assertEqual(res.count("n_1"), 1)
        self.assertEqual(res.count("n_2"), 1)

    def test_field_double_rendering_id_class(self):
        res = render_form(
            '{{ form.simple }}'
            '{% render_field form.simple id="id_1" class="c_1" %}'
            '{% render_field form.simple id="id_2" class="c_2" %}'
        )
        self.assertEqual(res.count("id_1"), 1)
        self.assertEqual(res.count("id_2"), 1)
        self.assertEqual(res.count("c_1"), 1)
        self.assertEqual(res.count("c_2"), 1)

    def test_field_double_rendering_name_class(self):
        res = render_form(
            '{{ form.simple }}'
            '{% render_field form.simple name="n_1" class="c_1" %}'
            '{% render_field form.simple name="n_2" class="c_2" %}'
        )
        self.assertEqual(res.count("n_1"), 1)
        self.assertEqual(res.count("n_2"), 1)
        self.assertEqual(res.count("c_1"), 1)
        self.assertEqual(res.count("c_2"), 1)


class RenderFieldTagUseTemplateVariableTest(TestCase):
    def test_use_template_variable_in_parametrs(self):
        res = render_form('{% render_field form.with_attrs egg+="pahaz" placeholder=form.with_attrs.label %}')
        assertIn('egg="spam pahaz"', res)
        assertIn('placeholder="With attrs"', res)


class RenderFieldFilter_field_type_widget_type_Test(TestCase):
    def test_field_type_widget_type_rendering_simple(self):
        res = render_form('<div class="{{ form.simple|field_type }} {{ form.simple|widget_type }} {{ form.simple.html_name }}">{{ form.simple }}</div>')
        assertIn('class="charfield textinput simple"', res)


class RenderFieldTagNonValueAttribute(TestCase):
    def test_field_non_value(self):
        res = render_form('{{ form.simple|attr:"foo" }}')
        assertIn('foo', res)
        assertNotIn('foo=', res)

    def test_field_empty_value(self):
        res = render_form('{{ form.simple|attr:"foo:" }}')
        assertIn('foo=""', res)

    def test_field_other_value(self):
        res = render_form('{{ form.simple|attr:"foo:bar" }}')
        assertIn('foo="bar"', res)

    def test_field_double_colon(self):
        res = render_form('{{ form.simple|attr:"v-bind::class:value" }}')
        assertIn('v-bind:class="value"', res)

    def test_field_double_colon_morethanone(self):
        res = render_form('{{ form.simple|attr:"v-bind::class:{active:True}" }}')
        assertIn('v-bind:class="{active:True}"', res)
    def test_field_arroba(self):
        res = render_form('{{ form.simple|attr:"@click:onClick" }}')
        assertIn('@click="onClick"', res)
    def test_field_arroba_dot(self):
        res = render_form('{{ form.simple|attr:"@click.prevent:onClick" }}')
        assertIn('@click.prevent="onClick"', res)

    def test_field_double_colon_missing(self):
        res = render_form('{{ form.simple|attr:"::class:{active:True}" }}')
        assertIn(':class="{active:True}"', res)


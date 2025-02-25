from unittest import TestCase

from .forms import render_field, render_field_from_tag, render_form, MyForm


def assertIn(value, obj):
    assert value in obj, "%s not in %s" % (value, obj)


def assertNotIn(value, obj):
    assert value not in obj, "%s in %s" % (value, obj)


# ===============================
#           Test cases
# ===============================


class SimpleAttrTest(TestCase):
    def test_attr(self):
        res = render_field("simple", "attr", "foo:bar")
        assertIn('type="text"', res)
        assertIn('name="simple"', res)
        assertIn('id="id_simple"', res)
        assertIn('foo="bar"', res)

    def test_attr_chaining(self):
        res = render_field("simple", "attr", "foo:bar", "attr", "bar:baz")
        assertIn('type="text"', res)
        assertIn('name="simple"', res)
        assertIn('id="id_simple"', res)
        assertIn('foo="bar"', res)
        assertIn('bar="baz"', res)

    def test_add_class(self):
        res = render_field("simple", "add_class", "foo")
        assertIn('class="foo"', res)

    def test_add_multiple_classes(self):
        res = render_field("simple", "add_class", "foo bar")
        assertIn('class="foo bar"', res)

    def test_add_class_chaining(self):
        res = render_field("simple", "add_class", "foo", "add_class", "bar")
        assertIn('class="bar foo"', res)

    def test_set_data(self):
        res = render_field("simple", "set_data", "key:value")
        assertIn('data-key="value"', res)

    def test_replace_type(self):
        res = render_field("simple", "attr", "type:date")
        self.assertTrue(res.count("type=") == 1, (res, res.count("type=")))
        assertIn('type="date"', res)

    def test_replace_hidden(self):
        res = render_field("simple", "attr", "type:hidden")
        self.assertTrue(res.count("type=") == 1, (res, res.count("type=")))
        assertIn('type="hidden"', res)


class ErrorsTest(TestCase):
    def _err_form(self):
        form = MyForm({"foo": "bar"})  # some random data
        form.is_valid()  # trigger form validation
        return form

    def test_error_class_no_error(self):
        res = render_field("simple", "add_error_class", "err")
        assertNotIn('class="err"', res)

    def test_error_class_error(self):
        form = self._err_form()
        res = render_field("simple", "add_error_class", "err", form=form)
        assertIn('class="err"', res)

    def test_required_class(self):
        res = render_field("simple", "add_required_class", "is-required")
        assertIn('class="is-required"', res)

    def test_required_class_requiredfield(self):
        form = self._err_form()
        res = render_field("simple", "add_required_class", "is-required", form=form)
        assertIn('class="is-required"', res)
        assertIn("required", res)

    def test_error_attr_no_error(self):
        res = render_field("simple", "add_error_attr", "aria-invalid:true")
        assertNotIn('aria-invalid="true"', res)

    def test_error_attr_error(self):
        form = self._err_form()
        res = render_field("simple", "add_error_attr", "aria-invalid:true", form=form)
        assertIn('aria-invalid="true"', res)


class SilenceTest(TestCase):
    def test_silence_without_field(self):
        res = render_field("nothing", "attr", "foo:bar")
        self.assertEqual(res, "")
        res = render_field("nothing", "add_class", "some")
        self.assertEqual(res, "")
        res = render_field("nothing", "remove_attr", "some")
        self.assertEqual(res, "")


class CustomizedWidgetTest(TestCase):
    def test_attr(self):
        res = render_field("with_attrs", "attr", "foo:bar")
        assertIn('foo="bar"', res)
        assertNotIn('foo="baz"', res)
        assertIn('egg="spam"', res)

    def test_attr_chaining(self):
        res = render_field("with_attrs", "attr", "foo:bar", "attr", "bar:baz")
        assertIn('foo="bar"', res)
        assertNotIn('foo="baz"', res)
        assertIn('egg="spam"', res)
        assertIn('bar="baz"', res)

    def test_attr_class(self):
        res = render_field("with_cls", "attr", "foo:bar")
        assertIn('foo="bar"', res)
        assertIn('class="class0"', res)

    def test_default_attr(self):
        res = render_field("with_cls", "attr", "type:search")
        assertIn('class="class0"', res)
        assertIn('type="search"', res)

    def test_add_class(self):
        res = render_field("with_cls", "add_class", "class1")
        assertIn("class0", res)
        assertIn("class1", res)

    def test_add_class_chaining(self):
        res = render_field("with_cls", "add_class", "class1", "add_class", "class2")
        assertIn("class0", res)
        assertIn("class1", res)
        assertIn("class2", res)

    def test_remove_attr(self):
        res = render_field("with_attrs", "remove_attr", "foo")
        assertNotIn("foo", res)


class FieldReuseTest(TestCase):
    def test_field_double_rendering_simple(self):
        res = render_form(
            '{{ form.simple }}{{ form.simple|attr:"foo:bar" }}{{ form.simple }}'
        )
        self.assertEqual(res.count("bar"), 1)

    def test_field_double_rendering_simple_css(self):
        res = render_form(
            '{{ form.simple }}{{ form.simple|add_class:"bar" }}{{ form.simple|add_class:"baz" }}'
        )
        self.assertEqual(res.count("baz"), 1)
        self.assertEqual(res.count("bar"), 1)

    def test_field_double_rendering_attrs(self):
        res = render_form(
            '{{ form.with_cls }}{{ form.with_cls|add_class:"bar" }}{{ form.with_cls }}'
        )
        self.assertEqual(res.count("class0"), 3)
        self.assertEqual(res.count("bar"), 1)


class SimpleRenderFieldTagTest(TestCase):
    def test_attr(self):
        res = render_field_from_tag("simple", 'foo="bar"')
        assertIn('type="text"', res)
        assertIn('name="simple"', res)
        assertIn('id="id_simple"', res)
        assertIn('foo="bar"', res)

    def test_multiple_attrs(self):
        res = render_field_from_tag("simple", 'foo="bar"', 'bar="baz"')
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
        res = render_field_from_tag("with_attrs", 'foo="bar"')
        assertIn('foo="bar"', res)
        assertNotIn('foo="baz"', res)
        assertIn('egg="spam"', res)

    def test_multiple_attrs(self):
        res = render_field_from_tag("with_attrs", 'foo="bar"', 'bar="baz"')
        assertIn('foo="bar"', res)
        assertNotIn('foo="baz"', res)
        assertIn('egg="spam"', res)
        assertIn('bar="baz"', res)

    def test_attr_class(self):
        res = render_field_from_tag("with_cls", 'foo="bar"')
        assertIn('foo="bar"', res)
        assertIn('class="class0"', res)

    def test_default_attr(self):
        res = render_field_from_tag("with_cls", 'type="search"')
        assertIn('class="class0"', res)
        assertIn('type="search"', res)

    def test_append_attr(self):
        res = render_field_from_tag("with_cls", 'class+="class1"')
        assertIn("class0", res)
        assertIn("class1", res)

    def test_duplicate_append_attr(self):
        res = render_field_from_tag("with_cls", 'class+="class1"', 'class+="class2"')
        assertIn("class0", res)
        assertIn("class1", res)
        assertIn("class2", res)

    def test_hyphenated_attributes(self):
        res = render_field_from_tag("with_cls", 'data-foo="bar"')
        assertIn('data-foo="bar"', res)
        assertIn('class="class0"', res)

    def test_alpinejs_event_modifier(self):
        res = render_field_from_tag(
            "simple", '@click.away="open=false"', 'x-on::click.away="open=false"'
        )
        assertIn('@click.away="open=false"', res)
        assertIn('x-on:click.away="open=false"', res)


class RenderFieldWidgetClassesTest(TestCase):
    def test_use_widget_required_class(self):
        res = render_form(
            "{% render_field form.simple %}", WIDGET_REQUIRED_CLASS="required_class"
        )
        assertIn('class="required_class"', res)

    def test_use_widget_error_class(self):
        res = render_form(
            "{% render_field form.simple %}",
            form=MyForm({}),
            WIDGET_ERROR_CLASS="error_class",
        )
        assertIn('class="error_class"', res)

    def test_use_widget_error_class_with_other_classes(self):
        res = render_form(
            '{% render_field form.simple class="blue" %}',
            form=MyForm({}),
            WIDGET_ERROR_CLASS="error_class",
        )
        assertIn('class="blue error_class"', res)

    def test_use_widget_required_class_with_other_classes(self):
        res = render_form(
            '{% render_field form.simple class="blue" %}',
            form=MyForm({}),
            WIDGET_REQUIRED_CLASS="required_class",
        )
        assertIn('class="blue required_class"', res)


class RenderFieldTagFieldReuseTest(TestCase):
    def test_field_double_rendering_simple(self):
        res = render_form(
            '{{ form.simple }}{% render_field form.simple foo="bar" %}{% render_field form.simple %}'
        )
        self.assertEqual(res.count("bar"), 1)

    def test_field_double_rendering_simple_css(self):
        res = render_form(
            '{% render_field form.simple %}{% render_field form.simple class+="bar" %}{% render_field form.simple class+="baz" %}'
        )
        self.assertEqual(res.count("baz"), 1)
        self.assertEqual(res.count("bar"), 1)

    def test_field_double_rendering_attrs(self):
        res = render_form(
            '{% render_field form.with_cls %}{% render_field form.with_cls class+="bar" %}{% render_field form.with_cls %}'
        )
        self.assertEqual(res.count("class0"), 3)
        self.assertEqual(res.count("bar"), 1)

    def test_field_double_rendering_id(self):
        res = render_form(
            "{{ form.simple }}"
            '{% render_field form.simple id="id_1" %}'
            '{% render_field form.simple id="id_2" %}'
        )
        self.assertEqual(res.count("id_1"), 1)
        self.assertEqual(res.count("id_2"), 1)

    def test_field_double_rendering_id_name(self):
        res = render_form(
            "{{ form.simple }}"
            '{% render_field form.simple id="id_1" name="n_1" %}'
            '{% render_field form.simple id="id_2" name="n_2" %}'
        )
        self.assertEqual(res.count("id_1"), 1)
        self.assertEqual(res.count("id_2"), 1)
        self.assertEqual(res.count("n_1"), 1)
        self.assertEqual(res.count("n_2"), 1)

    def test_field_double_rendering_id_class(self):
        res = render_form(
            "{{ form.simple }}"
            '{% render_field form.simple id="id_1" class="c_1" %}'
            '{% render_field form.simple id="id_2" class="c_2" %}'
        )
        self.assertEqual(res.count("id_1"), 1)
        self.assertEqual(res.count("id_2"), 1)
        self.assertEqual(res.count("c_1"), 1)
        self.assertEqual(res.count("c_2"), 1)

    def test_field_double_rendering_name_class(self):
        res = render_form(
            "{{ form.simple }}"
            '{% render_field form.simple name="n_1" class="c_1" %}'
            '{% render_field form.simple name="n_2" class="c_2" %}'
        )
        self.assertEqual(res.count("n_1"), 1)
        self.assertEqual(res.count("n_2"), 1)
        self.assertEqual(res.count("c_1"), 1)
        self.assertEqual(res.count("c_2"), 1)

    def test_field_double_rendering_simple_again(self):
        res = render_form('{% render_field form.simple foo="bar" v-model="username" %}')
        self.assertEqual(res.count('v-model="username"'), 1)


class RenderFieldTagUseTemplateVariableTest(TestCase):
    def test_use_template_variable_in_parameters(self):
        res = render_form(
            '{% render_field form.with_attrs egg+="pahaz" placeholder=form.with_attrs.label %}'
        )
        assertIn('egg="spam pahaz"', res)
        assertIn('placeholder="With attrs"', res)


class RenderFieldFilter_field_type_widget_type_Test(TestCase):
    def test_field_type_widget_type_rendering_simple(self):
        res = render_form(
            '<div class="{{ form.simple|field_type }} {{ form.simple|widget_type }} {{ form.simple.html_name }}">{{ form.simple }}</div>'
        )
        assertIn('class="charfield textinput simple"', res)


class RenderFieldTagNonValueAttribute(TestCase):
    def test_field_non_value(self):
        res = render_form('{{ form.simple|attr:"foo" }}')
        assertIn("foo", res)
        assertNotIn("foo=", res)

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

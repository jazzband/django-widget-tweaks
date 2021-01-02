import string
from django import forms
from django.forms import Form, CharField, SelectDateWidget, TextInput
from django.template import Template, Context


class MyForm(Form):
    """
    Test form. If you want to test rendering of a field,
    add it to this form and use one of 'render_...' functions
    from this module.
    """

    simple = CharField()
    with_attrs = CharField(widget=TextInput(attrs={"foo": "baz", "egg": "spam"}))
    with_cls = CharField(widget=TextInput(attrs={"class": "class0"}))
    date = forms.DateField(widget=SelectDateWidget(attrs={"egg": "spam"}))


def render_form(text, form=None, **context_args):
    """
    Renders template ``text`` with widget_tweaks library loaded
    and MyForm instance available in context as ``form``.
    """
    tpl = Template("{% load widget_tweaks %}" + text)
    context_args.update({"form": MyForm() if form is None else form})
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
    filter_strings = ['|%s:"%s"' % (f[0], f[1]) for f in filters]
    render_field_str = "{{ form.%s%s }}" % (field, "".join(filter_strings))
    return render_form(render_field_str, **kwargs)


def render_field_from_tag(field, *attributes):
    """
    Renders MyForm's field ``field`` with attributes passed
    as positional arguments.
    """
    attr_strings = [" %s" % f for f in attributes]
    tpl = string.Template("{% render_field form.$field$attrs %}")
    render_field_str = tpl.substitute(field=field, attrs="".join(attr_strings))
    return render_form(render_field_str)

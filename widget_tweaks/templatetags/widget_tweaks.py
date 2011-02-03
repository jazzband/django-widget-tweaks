from django.template import Library
register = Library()

def _process_field_attributes(field, attr, process):

    # split attribute name and value from 'attr:value' string
    params = attr.split(':', 1)
    attribute = params[0]
    value = params[1] if len(params) == 2 else ''

    # decorate field.as_widget method with updated attributes
    old_as_widget = field.as_widget
    def as_widget(self, widget=None, attrs=None, only_initial=False):
        attrs = attrs or {}
        process(widget or self.field.widget, attrs, attribute, value)
        return old_as_widget(widget, attrs, only_initial)

    bound_method = type(old_as_widget)
    field.as_widget = bound_method(as_widget, field, field.__class__)
    return field

@register.filter('attr')
def set_attr(field, attr):
    def process(widget, attrs, attribute, value):
        attrs[attribute] = value
    return _process_field_attributes(field, attr, process)

@register.filter
def append_attr(field, attr):
    def process(widget, attrs, attribute, value):
        if attrs.get(attribute):
            attrs[attribute] += ' ' + value
        elif widget.attrs.get(attribute):
            attrs[attribute] = widget.attrs[attribute] + ' ' + value
        else:
            attrs[attribute] = value
    return _process_field_attributes(field, attr, process)

@register.filter
def add_class(field, css_class):
    return append_attr(field, 'class:'+ css_class)

@register.filter
def set_data(field, data):
    return set_attr(field, 'data-' + data)

@register.filter
def behave(field, names):
    ''' https://github.com/anutron/behavior support '''
    return set_data(field, 'filters:'+names)

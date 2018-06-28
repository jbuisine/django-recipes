from django import template

register = template.Library()


@register.filter('duration_format')
def duration_format(value):
    value = int(value)

    hours = int(value / 60)
    minutes = value % 60

    if hours > 0:
        return '%s h %s min' % (hours, minutes)
    else:
        return '%s min' % minutes

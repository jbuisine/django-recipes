from django import template

from recipes.models import RecipeType, RecipeDifficulty

register = template.Library()


@register.inclusion_tag('recipes/partials/nav.html', takes_context=True)
def navigation(context):
    return {
        'recipe_types': RecipeType.objects.all(),
        'recipe_difficulties': RecipeDifficulty.objects.all(),
        'user': context['request'].user,
        'request': context['request']
    }


@register.filter('duration_format')
def duration_format(value):
    value = int(value)

    hours = int(value / 60)
    minutes = value % 60

    if hours > 0:
        return '%s h %s min' % (hours, minutes)
    else:
        return '%s min' % minutes

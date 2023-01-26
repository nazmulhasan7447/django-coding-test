from django import template

register = template.Library()

@register.filter()
def showing_objects_starting_range(previous_page_num):

    return (previous_page_num * 3) + 1


@register.filter()
def showing_objects_ending_range(previous_page_num):

    return (previous_page_num + 1) * 3

@register.filter()
def showing_objects_ending_range_for_last_page(previous_page_num):

    return ((previous_page_num + 1) * 3)

# @register.simple_tag
# def showed_objects_ending_range_
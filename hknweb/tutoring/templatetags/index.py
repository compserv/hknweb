from django import template

register = template.Library()

@register.filter
def access_slot_at_hour(slots, hour):
    return slots[hour].order_by('day')
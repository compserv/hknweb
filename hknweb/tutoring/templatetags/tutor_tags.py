from django import template

register = template.Library()

@register.filter
def access_slot_at_hour(slots, hour):
    return slots[hour].order_by('timeslot__day')

@register.filter
def access_slotfields_at_hour(form, hour):
    slotfields = []
    for timeslot_id in range((hour-11)* 5 + 1, (hour-10) * 5 + 1):
        time_pref_field = form.fields['timeslot_time_preference_%s' % (timeslot_id,)]
        office_pref_field = form.fields['timeslot_office_preference_%s' % (timeslot_id,)]
        slotfields.append([time_pref_field, office_pref_field])
    return slotfields
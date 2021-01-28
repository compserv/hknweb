from django import template
from django.apps import apps

register = template.Library()
TimeSlot = apps.get_model('tutoring', 'TimeSlot')

@register.filter
def access_slot_at_hour(slots, hour):
    return slots[hour].order_by('timeslot__day')

@register.filter
def access_slotfields_at_hour(form, hour):
    slotfields = []
    hour_index = 0
    for hour_choice in TimeSlot.HOUR_CHOICES:
        if hour == hour_choice[0]:
            break
        hour_index += 1
    row_interval = len(TimeSlot.DAY_CHOICES)
    for timeslot_id in range(hour_index * row_interval, (hour_index + 1) * row_interval):
        fieldname = 'timeslot_time_preference_%s' % (timeslot_id,)
        time_pref_field = form.fields[fieldname].get_bound_field(form, fieldname)

        number_of_tutor_rooms = Room.objects.all().count()

        if number_of_tutor_rooms == 1:
            slotfields.append([time_pref_field])
        elif number_of_tutor_rooms == 2:
            fieldname = 'timeslot_office_preference_%s' % (timeslot_id,)
            office_pref_field = form.fields[fieldname].get_bound_field(form, fieldname)
            slotfields.append([time_pref_field, office_pref_field])
        else:
            # TODO: In the event there is multiple rooms (low priority)
            pass
    return slotfields

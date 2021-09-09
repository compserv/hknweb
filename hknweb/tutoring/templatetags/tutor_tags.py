from django import template
from django.apps import apps

register = template.Library()
TimeSlot = apps.get_model("tutoring", "TimeSlot")
Room = apps.get_model("tutoring", "Room")


@register.filter
def access_slot_at_hour(slots, hour):
    return slots[hour].order_by("timeslot__day")


@register.filter
def access_slotfields_at_hour(form, hour):
    slotfields = []
    hour_index = 0
    for hour_choice in TimeSlot.HOUR_CHOICES:
        if hour == hour_choice[0]:
            break
        hour_index += 1
    row_interval = len(TimeSlot.DAY_CHOICES)
    for timeslot_id in range(
        hour_index * row_interval, (hour_index + 1) * row_interval
    ):
        fieldname = "timeslot_time_preference_%s" % (timeslot_id,)

        time_pref_field = None
        if fieldname in form.fields:
            time_pref_field = form.fields[fieldname].get_bound_field(form, fieldname)

        # TODO: TO BE UNCOMMENTED ONCE A SOLUTION FOR MORE THAN ONE ROOM IS DECIDED
        # pref_fields = [time_pref_field]
        # for room in Room.objects.all():
        #     fieldname = "timeslot_office_preference_%s_%s" % (timeslot_id, room.id)
        #     if fieldname in form.fields:
        #         pref_fields.append(form.fields[fieldname].get_bound_field(form, fieldname))  
        
        # slotfields.append(pref_fields)
        fieldname = "timeslot_office_preference_%s" % (timeslot_id,)
        office_pref_field = None
        if fieldname in form.fields:
            office_pref_field = form.fields[fieldname].get_bound_field(form, fieldname)
        slotfields.append([time_pref_field, office_pref_field])

    return slotfields

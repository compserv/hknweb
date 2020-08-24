from django.db import models
from django.db.models import Count


class AcademicEntity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    """
    Merges two Academic entities of the same type.
    to_keep: the entity which should subsume the other one (take on all its children), and whose parent should remain
    to_remove: the entity which should be removed 
    """
    @staticmethod
    def merge(to_keep, to_remove):
        if len(to_remove) == 0:
            raise Exception()
        child_classes=to_remove[0].CHILDREN
        for child_class in child_classes:
            affected_children = getattr(to_remove[0],child_class+"_set")
            for dup in to_remove[1:]:
                affected_children = affected_children | getattr(dup,child_class+"_set")
            errors = affected_children.values(child_class+"_"+to_remove[0].__class__.__name__.lower()).annotate(count=Count("id")).filter(count__gt=1)

            if errors.exists():
                print(("Merge Conflict {}. There are two identical {}s.  {} ids: " + [x.id for x in errors]).format(
                    to_remove[0].__class__.__name__.lower()),child_class,child_class)
                return
            affected_children.update(**{child_class+"_"+to_remove[0].__class__.__name__.lower():to_keep})


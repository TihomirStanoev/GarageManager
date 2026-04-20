from django.core.exceptions import PermissionDenied, ValidationError


def _require_staff(user):
    if not user.is_staff:
        raise PermissionDenied("Only staff can permanently delete.")



def hard_delete_object(obj, user):
    _require_staff(user)

    if not obj.is_deleted:
        raise ValidationError("Object must be archived first.")

    obj.hard_delete()


def restore_object(obj, user):
    _require_staff(user)

    if not obj.is_deleted:
        raise ValidationError("Object is not archived and cannot be restored.")

    obj.restore()
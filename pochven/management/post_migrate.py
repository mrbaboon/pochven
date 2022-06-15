from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q


def register_permissions(sender, **kwargs):

    if sender.name != "pochven":
        return

    ct = ContentType.objects.get(app_label='pochven', model='permission')

    reset_scouts_perm, _ = Permission.objects.get_or_create(
        content_type=ct,
        codename='reset_scouts',
        defaults=dict(
            name='Reset Scouts',
        )
    )

    fc_group, _ = Group.objects.get_or_create(name='FC')
    fc_group.permissions.add(
        reset_scouts_perm
    )

    admin_permissions = Permission.objects.filter(
        Q(content_type__app_label__exact='auth',
          content_type__model__exact='user')
    )

    admin_group, _ = Group.objects.get_or_create(name='Admin')
    admin_group.permissions.add(
        reset_scouts_perm, *admin_permissions
    )

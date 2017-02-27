# Copyright (c) 2012-2017 Seafile Ltd.
import django.dispatch

admin_delete_repo = django.dispatch.Signal(providing_args=["admin_name", "repo_id"])
admin_transfer_repo = django.dispatch.Signal(providing_args=["admin_name", "repo_id", "from_email", "to_email"])

admin_create_group = django.dispatch.Signal(providing_args=["admin_name", "group_id"])
admin_transfer_group = django.dispatch.Signal(providing_args=["admin_name", "group_id", "from_email", "to_email"])
admin_delete_group = django.dispatch.Signal(providing_args=["admin_name", "group_id"])

admin_create_user = django.dispatch.Signal(providing_args=["admin_name", "new_user"])
admin_delete_user = django.dispatch.Signal(providing_args=["admin_name", "deleted_user"])

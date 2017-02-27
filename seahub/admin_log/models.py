# Copyright (c) 2012-2017 Seafile Ltd.
import json
import datetime

from django.db import models
from django.db.models import Q

## admin operation type

# detail: {'repo_id': repo_id, 'from': from_user, 'to': to_user}
ADMIN_OP_TYPE_TRANSFER_REPO = 'transfer_repo'

# detail: {'repo_id': repo_id}
ADMIN_OP_TYPE_DELETE_REPO = 'delete_repo'

# detail: {'group_id': group_id}
ADMIN_OP_TYPE_CREATE_GROUP = 'create_group'

# detail: {'group_id': group_id, 'from': from_user, 'to': to_user}
ADMIN_OP_TYPE_TRANSFER_GROUP = 'transfer_group'

# detail: {'group_id': group_id}
ADMIN_OP_TYPE_DELETE_GROUP = 'delete_group'

# detail: {'email': new_user}
ADMIN_OP_TYPE_CREATE_USER = 'create_user'

# detail: {'email': deleted_user}
ADMIN_OP_TYPE_DELETE_USER = 'delete_user'


class AdminLogManager(models.Manager):

    def add_admin_log(self, email, operation, detail):

        model= super(AdminLogManager, self).create(
            email=email, operation=operation, detail=detail)

        model.save()

        return model

    def get_admin_logs(self, email=None, operation=None):

        logs = super(AdminLogManager, self).all()

        if email and operation:
            filtered_logs = logs.filter(Q(email=email) & Q(operation = operation))
        elif email:
            filtered_logs = logs.filter(email=email)
        elif operation:
            filtered_logs = logs.filter(operation=operation)
        else:
            filtered_logs = logs

        return filtered_logs

class AdminLog(models.Model):
    email = models.EmailField(db_index=True)
    operation = models.CharField(max_length=255, db_index=True)
    detail = models.CharField(max_length=255)
    datetime = models.DateTimeField(default=datetime.datetime.now)
    objects = AdminLogManager()

    class Meta:
        ordering = ["-datetime"]


###### signal handlers
from django.dispatch import receiver
from seahub.admin_log.signals import admin_transfer_repo, admin_delete_repo, \
        admin_create_group, admin_transfer_group, admin_delete_group,\
        admin_create_user, admin_delete_user

@receiver(admin_transfer_repo)
def admin_transfer_repo_cb(sender, **kwargs):
    admin_name = kwargs['admin_name']
    repo_id = kwargs['repo_id']
    from_email = kwargs['from_email']
    to_email = kwargs['to_email']

    detail = {
        'repo_id': repo_id,
        'from': from_email,
        'to': to_email,
    }

    detail_json = json.dumps(detail)
    AdminLog.objects.add_admin_log(admin_name,
            ADMIN_OP_TYPE_TRANSFER_REPO, detail_json)

@receiver(admin_delete_repo)
def admin_delete_repo_cb(sender, **kwargs):
    admin_name = kwargs['admin_name']
    repo_id = kwargs['repo_id']

    detail = {'repo_id': repo_id}
    detail_json = json.dumps(detail)

    AdminLog.objects.add_admin_log(admin_name,
            ADMIN_OP_TYPE_DELETE_REPO, detail_json)

@receiver(admin_create_group)
def admin_create_group_cb(sender, **kwargs):
    admin_name = kwargs['admin_name']
    group_id = kwargs['group_id']

    detail = {'group_id': group_id}
    detail_json = json.dumps(detail)

    AdminLog.objects.add_admin_log(admin_name,
            ADMIN_OP_TYPE_CREATE_GROUP, detail_json)

@receiver(admin_transfer_group)
def admin_transfer_group_cb(sender, **kwargs):
    admin_name = kwargs['admin_name']
    group_id = kwargs['group_id']
    from_email = kwargs['from_email']
    to_email = kwargs['to_email']

    detail = {
        'group_id': group_id,
        'from': from_email,
        'to': to_email,
    }

    detail_json = json.dumps(detail)
    AdminLog.objects.add_admin_log(admin_name,
            ADMIN_OP_TYPE_TRANSFER_GROUP, detail_json)

@receiver(admin_delete_group)
def admin_delete_group_cb(sender, **kwargs):
    admin_name = kwargs['admin_name']
    group_id = kwargs['group_id']

    detail = {'group_id': group_id}
    detail_json = json.dumps(detail)

    AdminLog.objects.add_admin_log(admin_name,
            ADMIN_OP_TYPE_DELETE_GROUP, detail_json)

@receiver(admin_create_user)
def admin_create_user_cb(sender, **kwargs):
    admin_name = kwargs['admin_name']
    new_user = kwargs['new_user']

    detail = {'email': new_user}
    detail_json = json.dumps(detail)

    AdminLog.objects.add_admin_log(admin_name,
            ADMIN_OP_TYPE_CREATE_USER, detail_json)

@receiver(admin_delete_user)
def admin_delete_user_cb(sender, **kwargs):
    admin_name = kwargs['admin_name']
    deleted_user = kwargs['deleted_user']

    detail = {'email': deleted_user}
    detail_json = json.dumps(detail)

    AdminLog.objects.add_admin_log(admin_name,
            ADMIN_OP_TYPE_DELETE_USER, detail_json)

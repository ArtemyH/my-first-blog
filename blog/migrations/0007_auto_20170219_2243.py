# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('blog', '0006_auto_20170218_2252'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtUser',
            fields=[
                ('user_ptr', models.OneToOneField(to=settings.AUTH_USER_MODEL, serialize=False, auto_created=True, parent_link=True, primary_key=True)),
                ('phone_number', models.CharField(max_length=12)),
                ('skype', models.CharField(max_length=30, null=True)),
                ('avatar', models.ImageField(null=True, upload_to='')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]

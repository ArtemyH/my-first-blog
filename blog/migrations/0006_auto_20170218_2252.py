# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20170218_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='skype',
            field=models.CharField(null=True, max_length=30),
        ),
    ]

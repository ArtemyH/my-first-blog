# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20170222_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypost',
            name='rejected_reason',
            field=models.TextField(default=''),
        ),
    ]

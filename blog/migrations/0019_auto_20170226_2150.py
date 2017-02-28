# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20170225_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mypost',
            name='category',
            field=models.ForeignKey(to='blog.Category', blank=True, null=True),
        ),
    ]

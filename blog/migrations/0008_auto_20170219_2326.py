# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20170219_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extuser',
            name='phone_number',
            field=models.CharField(max_length=13),
        ),
    ]

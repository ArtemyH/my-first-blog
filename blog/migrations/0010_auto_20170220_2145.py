# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20170220_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extuser',
            name='avatar',
            field=models.ImageField(upload_to='user_media', null=True),
        ),
    ]

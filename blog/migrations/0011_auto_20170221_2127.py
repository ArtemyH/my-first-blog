# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20170220_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extuser',
            name='avatar',
            field=models.ImageField(upload_to='user_media', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='extuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='extuser',
            name='skype',
            field=models.CharField(null=True, blank=True, max_length=30),
        ),
    ]

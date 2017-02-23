# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20170222_0151'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypost',
            name='status',
            field=models.CharField(max_length=2, choices=[('IM', 'In moderation'), ('SM', 'Succesful moderation'), ('RM', 'Rejected')], default='IM'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(to='blog.MyPost', related_name='comments'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_mypost_rejected_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('value', models.IntegerField(default=0)),
                ('author', models.ForeignKey(to='blog.ExtUser')),
            ],
        ),
        migrations.AlterField(
            model_name='mypost',
            name='rejected_reason',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AddField(
            model_name='rating',
            name='post',
            field=models.ForeignKey(to='blog.MyPost'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-01-04 07:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='quanxian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('can_view', '查看'), ('can_add', '添加'), ('can_edit', '编辑'), ('can_delete', '删除')),
            },
        ),
    ]

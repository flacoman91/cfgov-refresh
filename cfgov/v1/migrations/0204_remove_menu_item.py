# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-02-26 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0203_deprecate_spanish_home_page'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='page_link',
        ),
        migrations.DeleteModel(
            name='MenuItem',
        ),
    ]

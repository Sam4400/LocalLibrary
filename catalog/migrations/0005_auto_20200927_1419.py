# Generated by Django 3.1.1 on 2020-09-27 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20200927_1304'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name', 'first_name'], 'permissions': (('can_add', 'Add Author'), ('can_delete', 'Delete Author'), ('can_edit', 'Edit Author'))},
        ),
    ]

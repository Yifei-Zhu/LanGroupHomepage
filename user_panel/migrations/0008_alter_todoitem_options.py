# Generated by Django 4.1 on 2024-03-04 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0007_todoitem_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todoitem',
            options={'ordering': ['order']},
        ),
    ]

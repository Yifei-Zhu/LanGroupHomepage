# Generated by Django 4.1 on 2024-03-04 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0006_remove_todoitem_completed_remove_todoitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]

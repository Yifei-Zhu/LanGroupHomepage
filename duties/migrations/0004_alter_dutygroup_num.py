# Generated by Django 4.1 on 2024-03-01 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duties', '0003_rename_sequence_dutygroup_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dutygroup',
            name='num',
            field=models.IntegerField(unique=True),
        ),
    ]

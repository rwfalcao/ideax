# Generated by Django 2.0.1 on 2018-04-13 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideax', '0010_auto_20180413_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='score',
            field=models.FloatField(default=0),
        ),
    ]

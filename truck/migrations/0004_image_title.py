# Generated by Django 3.1.5 on 2021-01-15 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truck', '0003_auto_20210115_0204'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='title',
            field=models.CharField(default=1, help_text='What is the pictures name.', max_length=75),
            preserve_default=False,
        ),
    ]
# Generated by Django 3.1.5 on 2021-01-29 22:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='What is the pictures name.', max_length=75)),
                ('link', models.URLField(help_text='Enter the target URL.', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(help_text='Enter the name of the dish.', max_length=75)),
                ('description', models.CharField(default='No description given.', help_text='Enter a description of the dish.', max_length=450)),
                ('cost', models.DecimalField(decimal_places=2, help_text='Enter the cost of the dish', max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='UserLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.DecimalField(decimal_places=22, max_digits=25)),
                ('lng', models.DecimalField(decimal_places=22, max_digits=25)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TruckInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the store name.', max_length=75)),
                ('location', models.CharField(default='Closed', help_text='Enter the current location.', max_length=75)),
                ('contact', models.CharField(blank=True, help_text='Enter a working number for the truck.', max_length=18)),
                ('album', models.ManyToManyField(blank=True, to='truck.ImageLink')),
                ('menu', models.ManyToManyField(blank=True, to='truck.MenuItem')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name', 'owner', 'location'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='truck.menuitem')),
            ],
        ),
        migrations.CreateModel(
            name='OrderInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prepared', models.BooleanField(default=False)),
                ('inventory', models.ManyToManyField(blank=True, to='truck.OrderItem')),
                ('poster', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('truck', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='truck.truckinstance')),
            ],
        ),
    ]

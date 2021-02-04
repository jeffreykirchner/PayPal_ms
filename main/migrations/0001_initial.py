# Generated by Django 3.1.5 on 2021-02-01 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parameters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contactEmail', models.CharField(default='JohnSmith@abc.edu', max_length=1000)),
                ('maxDailyEarnings', models.DecimalField(decimal_places=2, default=20, max_digits=5)),
                ('siteURL', models.CharField(default='https://www.google.com/', max_length=200)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Parameters',
                'verbose_name_plural': 'Parameters',
            },
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=1000)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('memo', models.CharField(default='', max_length=200)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
    ]
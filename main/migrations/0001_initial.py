# Generated by Django 4.2.dev20220912115206 on 2023-10-31 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_id', models.CharField(max_length=50)),
                ('artist_name', models.CharField(max_length=200)),
                ('bio', models.CharField(max_length=1000)),
            ],
        ),
    ]

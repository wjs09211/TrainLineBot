# Generated by Django 4.0.3 on 2022-03-22 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('code', models.IntegerField()),
            ],
            options={
                'db_table': 'station',
            },
        ),
        migrations.AddIndex(
            model_name='station',
            index=models.Index(fields=['name'], name='station_name_9ef58b_idx'),
        ),
    ]
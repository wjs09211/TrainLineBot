# Generated by Django 4.0.3 on 2022-03-25 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_id', models.CharField(max_length=64)),
                ('status', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'task',
            },
        ),
        migrations.AlterField(
            model_name='station',
            name='name',
            field=models.CharField(max_length=32),
        ),
    ]
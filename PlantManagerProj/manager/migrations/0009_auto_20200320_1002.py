# Generated by Django 3.0.3 on 2020-03-20 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manager', '0008_auto_20200318_2326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(max_length=50, unique=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['room'],
            },
        ),
        migrations.AddField(
            model_name='plant',
            name='location',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='location', to='manager.Location'),
        ),
    ]

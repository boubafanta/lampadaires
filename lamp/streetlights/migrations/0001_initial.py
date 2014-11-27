# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lampadaire',
            fields=[
                ('gid', models.IntegerField(serialize=False, primary_key=True)),
                ('ruleid', models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPointField(srid=32628, null=True, blank=True)),
            ],
            options={
                'db_table': 'lampadaire',
                'managed': True,
            },
            bases=(models.Model,),
        ),
    ]

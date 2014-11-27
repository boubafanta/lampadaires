# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streetlights', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lampadaire',
            name='states',
            field=models.CharField(default=b'ok', max_length=2, choices=[(b'ok', b'ok'), (b'bb', b'Broken Bulb'), (b'bl', b'Broken Light')]),
            preserve_default=True,
        ),
    ]

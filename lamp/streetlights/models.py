from django.db import models
from django.contrib.gis.db import models
# Create your models here.

class Lampadaire(models.Model):
    STATE = (
            ('ok', 'ok'),
            ('bb', 'Broken Bulb'),
            ('bl', 'Broken Light'),
        )
    gid = models.IntegerField(primary_key=True)
    ruleid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    states = models.CharField(max_length=2, choices=STATE, default='ok')
    geom = models.MultiPointField(srid=32628, blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        managed = True
        db_table = 'lampadaire'

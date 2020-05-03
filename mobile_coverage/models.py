from django.contrib.gis.db import models


PROVIDER_MAP = {
    20801: "orange",
    20810: "sfr",
    20815: "free",
    20820: "bouygues",
}


class MobileCoverage(models.Model):
    """Mobile coverage from a specific point for a specific provider
    """

    location = models.PointField(spatial_index=True)
    provider = models.IntegerField()
    has_2g = models.BooleanField()
    has_3g = models.BooleanField()
    has_4g = models.BooleanField()

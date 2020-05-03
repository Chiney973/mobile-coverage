import requests
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point

from mobile_coverage.models import MobileCoverage
from mobile_coverage.models import PROVIDER_MAP

from mobile_coverage import AddressNotFound

ADDRESS_TO_LAT_LONG_CONVERTER_ENDPOINT = "https://api-adresse.data.gouv.fr/search/?q="


def get_geo_point_from_address(address):
    response = requests.get(ADDRESS_TO_LAT_LONG_CONVERTER_ENDPOINT + address)
    data = response.json()
    try:
        longitude = data["features"][0]["geometry"]["coordinates"][0]
        latitude = data["features"][0]["geometry"]["coordinates"][1]
    except IndexError:
        raise AddressNotFound
    return Point(y=latitude, x=longitude, srid=4326)


def get_closest_provider_coverage_from_point(provider_id, point):
    coverage = MobileCoverage.objects.filter(provider=provider_id).annotate(
        distance=Distance("location", point)
    ).order_by("distance").first()
    distance_in_km = coverage.distance.m / 1000.0
    return {
        "2G": coverage.has_2g,
        "3G": coverage.has_3g,
        "4g": coverage.has_4g,
        "distance": float("%.3f" % distance_in_km),
    }


def get_closest_coverage_for_each_provider_from_point(point):
    providers_coverage ={}
    for provider_id, provider_name in PROVIDER_MAP.items():
        coverage = get_closest_provider_coverage_from_point(provider_id, point)
        providers_coverage[provider_name] = coverage
    return providers_coverage

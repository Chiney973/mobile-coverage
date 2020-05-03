import csv

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from mobile_coverage.models import MobileCoverage


class Command(BaseCommand):
    """Store lambert 93 point with srid 2154 (EPSG reference)
    source: https://epsg.io/2154
    Also verified with GDAL API
    ```
        $shell-prompt>from django.contrib.gis.gdal import SpatialReference
        $shell-prompt>ref = SpatialReference('EPSG:2154')
        $shell-prompt->ref.srid
        2154
        $shell-prompt->ref.proj4
        '+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs '
    ```
    Last line of shell is same as formula given in instruction
    https://docs.google.com/document/d/1sxNf2fC7rvhxmbd85t7O-oDv3OOJ21sH_QSfmZuIIb0/edit
    """
    help = """Load mobile coverage csv to database
    datasource is
    https://www.data.gouv.fr/s/resources/monreseaumobile/20180228-174515/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv
    """

    def add_arguments(self, parser):
        parser.add_argument("csv", type=str)

    def handle(self, *args, **options):
        filename = options["csv"]
        with open(filename) as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=";")
            for row in csv_reader:
                try:
                    # See explanation in doctring for why usage of srid=2154
                    point = Point(x=int(row[1]), y=int(row[2]), srid=2154)
                    MobileCoverage(
                        location=point,
                        provider=int(row[0]),
                        has_2g=bool(int(row[3])),
                        has_3g=bool(int(row[4])),
                        has_4g=bool(int(row[5]))
                    ).save()
                except Exception as e:
                    print("Could not process line")
                    print(row)
                    print(e)
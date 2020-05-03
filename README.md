# MobileCoverage

A simple web api to see mobile network coverage in France
Given an address, the api returns the mobile network coverage from
the main providers and distance in km from the closest source

## Stack

This project makes use of Django, DRF, GeoDjango, and Spatialite

## How to use
As we are using geodjango and spatialite,
you will need to have gdal dynamic library to run projet

Instructions to install it can be found in [Django official documentation](https://docs.djangoproject.com/en/3.0/ref/contrib/gis/install/spatialite/)


Launch these commands to run project
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Network coverage data
The source of network coverage is extracted from [data.gouv.fr](https://www.data.gouv.fr/s/resources/monreseaumobile/20180228-174515/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv)
An django command is available for parsing the csv and filling spatialite db.

Used as such:
```
pythom manage.py load_mobile_coverage_csv_to_database {csv_filename}
```

Or to make it simplier, fixture is provided in this repo
```
python manage.py loaddata data_gouv
```

## API

Usage examples

Try it with a densely covered network area in Paris
```
curl http://127.0.0.1:8000/coverage?q=21+Avenue+d+Italie,+75013+Paris | json_pp
{
    "orange": {
        "2G": false,
        "3G": true,
        "4g": true,
        "distance": 0.133
    },
    "sfr": {
        "2G": true,
        "3G": true,
        "4g": true,
        "distance": 0.12
    },
    "free": {
        "2G": false,
        "3G": true,
        "4g": true,
        "distance": 0.247
    },
    "bouygues": {
        "2G": true,
        "3G": true,
        "4g": true,
        "distance": 0.188
    }
}
```
Let's try with: Rue de l'Église, Plœuc-sur-Lié, Plœuc-L'Hermitage,
Saint-Brieuc, Côtes-d'Armor, Bretagne, France métropolitaine, 22150, France

A poorly covered network zone in Bretagne with coverage source with
distance superior to 1km
```
curl http://127.0.0.1:8000/coverage?q=Rue%20de%20l%27%C3%89glise,%20Pl%C5%93uc-sur-Li%C3%A9,%20Pl%C5%93uc-L%27Hermitage,%20Saint-Brieuc,%20C%C3%B4tes-d%27Armor,%20Bretagne,%20France%20m%C3%A9tropolitaine,%2022150,%20France | json_pp
{
   "free" : {
      "4g" : true,
      "2G" : false,
      "3G" : true,
      "distance" : 2.58
   },
   "bouygues" : {
      "4g" : false,
      "2G" : true,
      "3G" : true,
      "distance" : 2.575
   },
   "sfr" : {
      "2G" : true,
      "3G" : true,
      "distance" : 2.557,
      "4g" : false
   },
   "orange" : {
      "4g" : true,
      "3G" : true,
      "distance" : 2.275,
      "2G" : true
   }
}
```


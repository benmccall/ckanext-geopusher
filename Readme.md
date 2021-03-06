Geopusher
=========
Capture any KML/Shapefiles uploaded to CKAN and re-upload them as new GeoJSON resources

Implemented as a CKAN celery task that listens to resource updates

Installation
============
```
pip install -r requirements.txt
python setup.py develop
```
You will need GDAL. You can get in on Ubuntu with `apt-get install gdal-bin`

Then, add `geopusher` to your list of CKAN extensions:

```
ckan.plugins = ... geopusher
```

Usage
=====
### Automatic conversion
You can run the built-in CKAN celery daemon, if you want shapefiles and KML
resources to be converted automatically when they are created or updated:

```
paster --plugin=ckan celeryd -c development.ini
```

or if you are using [datacats](https://github.com/datacats/datacats):

```
datacats paster celeryd
```

### Batch jobs
To create a GeoJSON resource from all the Shapefile resources on your CKAN
server:
```
geopusher import --all -r http://myckan.org -a your_api_key
```

To only convert resources for a subset of datasets:
```
geopusher import dataset1 dataset2 dataset3 -r http://myckan.org -a your_api_key
=======
```
$ datacats paster celeryd
```

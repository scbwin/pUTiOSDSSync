# pUTiOSDSSync

## About pUTiOSDSSync

This is a small python app that monitors pUT.iO RSS feeds and synchronizes new items to a Synology Download Station.
It performs rudimentary cleanup: removing completed downloads from the download station and cleaning up pUT.iO directories.

## Dependencies

This project makes use of Python 2 and is highly dependant on:
- https://github.com/thavel/synolopy
- https://github.com/cenkalti/putio.py

Check the requirements.txt for other dependencies.

## Getting started
1. Check out the repository
2. Create an OATH app on pUT.iO
    1. From your pUT.iO -> Account -> Manage your applications -> Create a new OATH app
    2. Fill in Application name
    3. Fill in Description
    4. Save
    5. Make a note of the OATH token as it will be needed later
3. Obtain RSS feeds from pUT.iO
    1. Go to the folder on pUT.iO for which downloads should automatically be queued
    2. Actions -> RSS Feed -> Select the type of feed
    3. Take the RSS feed supplied and modify it so that it follows the format: `https:<putio_username>:<putio_password>@put.io/rss/<type>/<id>`
    4. Perform these actions for all of the folders for which downloads should automatically be queued
4. Edit config.yml
    1. Replace <your_synology_nas_ip> with the ip address of your diskstation on the local network
    2. Replace <your_synology_nas_username> and <your_synology_nas_password> with your diskstation's credentials
    3. Replace <your_putio_oath_token> with the token obtained in step 2
    4. Replace the feeds list with your feeds as obtained in step 3
5. Run app using Docker or Python

### Running using Docker
1. Build the image using `docker build -t putio_sds_sync`
2. Run the image using `docker run -d puio_sds_sync`

### Running using Python
1. Set up a python virtualenv if wanted
2. Install the dependencies using `pip install -r requirements.txt`
3. Run the app using `python app`

### Running tests
- Running all tests: `nosetests`
- Running all tests with coverage: `nosetests -s --with-coverage --cover-package=app`

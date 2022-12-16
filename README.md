# portico
This is a plugin for Janeway that produces zip files for depositing with the Portico service.

This plugin provides both Issue and Article level deposit formats. The archives are sent to portico via SFTP, for which you will need to request
a set of SSH credentials.

## Installation

* Copy the plugin under the plugins directory in your Janeway installation `/path/to/janeway/src/plugins/`
* Install this plugin's requirements with `pip install -r src/plugins/portico`
* Run Janeway's plugin install command: `python src/manage.py install_plugins`
* Run migrations: `python src/manage.py migrate portico`
* Configre the following settings under your Janeway project `settings.py` module:
```
PORTICO_FTP_SERVER = ''
PORTICO_FTP_SERVER_KEY = ''
PORTICO_FTP_USERNAME = ''
PORTICO_FTP_PASSWORD = ''
```
* Restart your Janeway instance

## ECDSA Key

As of late 2022 Portico only supports SFTP, so you will need to get the ECDSA key for their server before depositing. You can get the key by running:

```
ssh-keyscan -t ecdsa ftp.portico.org
```


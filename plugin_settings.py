from utils import models, setting_handler

PLUGIN_NAME = 'portico'
DESCRIPTION = 'This is a plugin to exporting Portico zip files.'
AUTHOR = 'Andy Byers'
VERSION = '1.0'
SHORT_NAME = 'portico'
DISPLAY_NAME = 'Portico'
MANAGER_URL = 'portico_index'

PORTICO_FTP_SERVER = ''
PORTICO_FTP_USERNAME = ''
PORTICO_FTP_PASSWORD = ''


def get_self():
    new_plugin, created = models.Plugin.objects.get_or_create(
        name=SHORT_NAME,
        display_name=DISPLAY_NAME,
        version=VERSION,
        enabled=True
    )
    return new_plugin


def install():
    new_plugin, created = models.Plugin.objects.get_or_create(
        name=SHORT_NAME,
        display_name=DISPLAY_NAME,
        version=VERSION,
        enabled=True
    )

    if created:
        print('Plugin {0} installed.'.format(PLUGIN_NAME))
    else:
        print('Plugin {0} is already installed.'.format(PLUGIN_NAME))


def hook_registry():
    # On site load, the load function is run for each installed plugin to
    # generate a list of hooks.
    return {}

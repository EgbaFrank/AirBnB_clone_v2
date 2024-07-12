#!/usr/bin/python3
"""
A Fabric script that generates a .tgz archive from
the web_static folder
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the web_static folder.

    Returns:
        str: The path to the created archive if successful, None otherwise.
    """
    dt = datetime.now().strftime("%Y%m%d%H%M%S")
    ar_name = "web_static_{}.tgz".format(dt)
    local('mkdir -p versions')
    result = local('tar -czvf versions/{} -C web_static .'.format(ar_name))

    if result.succeeded:
        print(f"Successfully created archive at versions/{ar_name}")
        return 'versions/{}'.format(ar_name)

    else:
        return None

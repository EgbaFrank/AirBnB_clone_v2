#!/usr/bin/python3
"""
A Fabric script that generates and distributes .tgz archive from
the web_static folder to web servers
"""
import os
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ['52.90.15.81', '18.204.11.162']
env.user = 'ubuntu'
env.key_filename = os.path.expanduser('~/.ssh/school')


def do_pack():
    """
    Generates a .tgz archive from the web_static folder.

    Returns:
        str: The path to the created archive if successful, None otherwise.
    """
    dt = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"web_static_{dt}.tgz"
    local('mkdir -p versions')
    result = local(f'tar -czvf versions/{archive_name} web_static')

    if result.succeeded:
        print(f"Successfully created archive at versions/{archive_name}")
        return f"versions/{archive_name}"

    else:
        return None


def do_deploy(archive_path):
    """
    Deploys the given archive to the remote server.

    Args:
        archive_path (str): The local path to archive to be distributed.

    Returns:
        Boolean: True if successful, False otherwise
    """
    # Check if the archive path exists locally
    if not os.path.exists(archive_path):
        print(f"File {archive_path} does not exist.")
        return False

    # Upload the archive to the /tmp/ directory on the remote server
    result = put(archive_path, '/tmp/')
    if result.failed:
        print(f"Failed to transfer archive")
        return False

    # Extract the name and base of the archive from the path
    archive_name = os.path.basename(archive_path)
    archive_base = os.path.splitext(archive_name)[0]
    remote_path = f"/tmp/{archive_name}"
    target_dir = f"/data/web_static/releases/{archive_base}"

    # Create the target directory where the archive will be extracted
    result = run(f"mkdir -p {target_dir}")
    if result.failed:
        print(f"Failed to create directory {target_dir}")
        return False

    # Extract the archive to the target directory
    result = run(f"tar -xzf {remote_path} -C {target_dir}")
    if result.failed:
        print(f"Failed to extract archive {remote_path}")
        return False

    # Remove the archive from the /tmp/ directory
    result = run(f"rm {remote_path}")
    if result.failed:
        print(f"Failed to remove archive {remote_path}")
        return False

    # Move contents of web_static folder to the target directory
    result = run(f"mv {target_dir}/web_static/* {target_dir}")
    if result.failed:
        print(f"Failed to move {target_dir}/web_static content")
        return False

    # Remove the now empty web_static directory
    result = run(f"rmdir {target_dir}/web_static")
    if result.failed:
        print(f"Failed to delete {target_dir}/web_static")
        return False

    # Remove the current symbolic link to the old release
    run("rm -f /data/web_static/current")

    # Create a new symbolic link to the new release
    result = run(f'ln -s {target_dir} /data/web_static/current')
    if result.failed:
        print(f"Failed to create symbolic link to {target_dir}")
        return False

    print("New version deployed!")
    return True

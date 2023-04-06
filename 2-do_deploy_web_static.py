#!/usr/bin/python3
"""Write a Fabric script (based on the file 1-pack_web_static.py) that
distributes an archive to your web servers, using the function do_deploy:
"""
# Prototype: def do_deploy(archive_path):
#   - Returns False if the file at the path archive_path doesn’t exist
#   - The script should take the following steps:
#   - Upload the archive to the /tmp/ directory of the web server
#   - Uncompress the archive to the
#     folder /data/web_static/releases/<archive filename without extension> on
#     the web server
#   - Delete the archive from the web server
#   - Delete the symbolic link /data/web_static/current from the web server
#   - Create a new the symbolic link /data/web_static/current on the web
#     server, linked to the new version of your
#     code (/data/web_static/releases/<archive filename without extension>)
#   - All remote commands must be executed on your both web servers (using
#     env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)
#   - Returns True if all operations have been done correctly, otherwise
#     returns False
#   - You must use this script to deploy it on your servers:
#     * xx-web-01 and
#     * xx-web-02

# In the following example, the SSH key and the username used for accessing to
# the server are passed in the command line. Of course, you could define them
# as Fabric environment variables (ex: env.user =...)
# Disclaimer: commands execute by Fabric displayed below are linked to the way
# we implemented the archive function do_pack - like the mv command - depending
# of your implementation of it, you may don’t need it
from fabric.api import put, env, cd, sudo

# Set env
env.hosts = ['18.207.139.229', '100.26.49.225']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """A function that distributes an archive to my webservers
    """
    if archive_path in [None, False]:
        return False

    # Get Archive Name
    archive_name = archive_path.split('/')[-1]
    unzipped_name = archive_name.split('.')[0]

    # Push to remote
    with cd('/tmp'):
        stat = put(local_path=archive_path, remote_path=archive_name,
                   use_sudo=True)
        if stat.failed:
            return False

    stat = sudo(
        'tar -xzf /tmp/{} -C /data/web_static/releases/'.format(archive_name))
    if stat.failed:
        return False

    stat = sudo('rm -fv /tmp/{}/'.format(archive_name))
    if stat.failed:
        return False

    # Deploy
    with cd('/data/web_static/'):
        stat = sudo('mkdir -p releases/{}/'.format(unzipped_name))
        if stat.failed:
            return False

        stat = sudo('cp -ru releases/web_static/* releases/{}/'.format(
            unzipped_name))
        if stat.failed:
            return False

        # Remove temporary files
        sudo('rm -rf releases/web_static/')

        # Create Symbolic link
        stat = sudo('rm -rf current')
        stat = sudo('ln -s releases/{}/ current'.format(unzipped_name))
        if stat.failed:
            return False

    return True

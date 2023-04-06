#!/usr/bin/python3
# Write a Fabric script (based on the file 2-do_deploy_web_static.py) that
# creates and distributes an archive to your web servers, using the function
# deploy:

# Prototype: def deploy():
#   - The script should take the following steps:
#     - Call the do_pack() function and store the path of the created archive
#     - Return False if no archive has been created
#     - Call the do_deploy(archive_path) function, using the new path of the
#       new archive
#     - Return the return value of do_deploy
#   - All remote commands must be executed on both of web your servers (using
#     env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)
#   - You must use this script to deploy it on your servers:
#     * xx-web-01 and
#     * xx-web-02

# In the following example, the SSH key and the username used for accessing to
# the server are passed in the command line.Of course, you could define them as
# Fabric environment variables (ex: env.user =…)
from fabric.api import env

env.user = 'ubuntu'
env.hosts = ['18.207.139.229', '100.26.49.225']
env.key_filename = '~/.ssh/id_rsa-alx_server_1'

do_pack = __import__("1-pack_web_static").do_pack
do_deploy = __import__('2-do_deploy_web_static').do_deploy

# import compressed file
archive_path = do_pack()


def deploy():
    """A function that creates and distributes an archive to my webserver
    using previously created functions
    """
    stat = do_deploy(archive_path)

    return stat

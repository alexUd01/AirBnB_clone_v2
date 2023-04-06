#!/usr/bin/python3
"""A Fabric script that generates a .tgz archive from the contents of the
web_static folder of my AirBnB Clone repo, using the function do_pack.
"""

# Prototype: def do_pack():
#     - All files in the folder web_static must be added to the final archive
#     - All archives must be stored in the folder versions (your function
#       should create this folder if it doesn’t exist)
#     - The name of the archive created must
#       be web_static_<year><month><day><hour><minute><second>.tgz
#     - The function do_pack must return the archive path if the archive has
#       been correctly generated. Otherwise, it should return None
from fabric.api import local, env
from time import strftime


def do_pack():
    """A function that generates a .tgz archive from contents of the web_static
    folder of my AirBnB Coloce repo
    """
    tstamp = strftime('%Y%m%d%H%M%S')

    cmd = "tar -cvzf versions/web_static_{}.tgz web_static".format(tstamp)
    path = cmd.split()[2]

    # Execute commands
    local("mkdir -p versions", capture=True)
    # print("Packing web_static to {}.tgz".format(path))
    stat = local(cmd, capture=False)
    # print("web_static packed: {} -> {}".format(path))

    return path if stat.succeeded else None

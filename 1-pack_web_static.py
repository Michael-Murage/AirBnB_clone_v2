#!/usr/bin/python3
"""
    generates a .tgz archive from the contents of the
     web_static folder of your AirBnB Clone repo, using the
     function do_pack.

    Prototype: def do_pack():
    All files in the folder web_static must be added to
     the final archive
    All archives must be stored in the folder versions
     (your function should create this folder if it doesn’t exist)
    The name of the archive created must be web_static
    _<year><month><day><hour><minute><second>.tgz
    The function do_pack must return the archive path if
     the archive has been correctly generated. Otherwise,
      it should return None
"""
import datetime
from fabric.api import local
from os.path import isdir


def do_pack():
    try:
        day_format = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        new_file = "versions/web_static_{}.tgz".format(day_format)
        local("tar -czvf {} web_static".format(new_file))
        return new_file
    except FileNotFoundError:
        return None

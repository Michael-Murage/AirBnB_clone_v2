#!/usr/bin/python3
"""
    Creates and distributes an archive to the web servers
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir
env.hosts = ['35.174.185.196', '54.157.141.97']
env.user = 'ubuntu'
env.identity = '~/.ssh/school'


def do_pack():
    """generates a tgz archive file"""
    try:
        day_format = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        new_file = "versions/web_static_{}.tgz".format(day_format)
        local("tar -czvf {} web_static".format(new_file))
        return new_file
    except FileNotFoundError:
        return None


def do_deploy(archive_path):
    """
        distributes an archive to your web servers,
         using the function do_deploy
    """

    if exists(archive_path) is False:
        return False
    try:
        new_file = archive_path.split("/")[-1]
        n = new_file.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("mkdir -p {}{}/".format(path, n))
        run('tar -xzf /tmp/{} -C {}{}/'.format(new_file, path, n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, n))
        run('rm -rf {}{}/web_static'.format(path, n))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, n))
        run('chmod -R 755 /data/')
        print("New version deployed!")
        return True
    except FileNotFoundError:
        return False


def deploy():
    """
        creates and distributes an archive to your web servers,
         using the function deploy
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

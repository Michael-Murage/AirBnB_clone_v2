#!/usr/bin/python3

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['3.230.144.5', '3.238.205.173']
env.user = 'ubuntu'
env.identity = '~/.ssh/school'
env.password = None


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

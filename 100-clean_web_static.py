#!/usr/bin/python3

import os, sys, getopt
from fabric.api import *

env.hosts = ['35.174.185.196', '54.157.141.97']
env.identity = '~/.ssh/school'


def do_clean(number=0):
    """
    Delete out-of-date archives.
    """
    try:
        arg, val = getopt.getopt(sys.argv[1:], "i:u:")
        ssh_key = None
        user = None
        for currArg, currVal in arg:
            if currArg in ("-i"):
                ssh_key = currVal
            elif currArg in ('-u'):
                user = currVal
        
        local("ssh {} -i {} -u {}".format(env.hosts[0] ,ssh_key, user))

        number = 1 if int(number) == 0 else int(number)

        all_archives = sorted(os.listdir("versions"))
        [all_archives.pop() for i in range(number)]
        with lcd("versions"):
            [local("rm ./{}".format(a)) for a in archives]

        with cd("/data/web_static/releases"):
            archives = run("ls -tr").split()
            archives = [a for a in archives if "web_static_" in a]
            [archives.pop() for i in range(number)]
            [run("rm -rf ./{}".format(a)) for a in archives]

        local("exit")

        local("ssh {} -i {} -u {}".format(env.hosts[1] ,ssh_key, user))

        number = 1 if int(number) == 0 else int(number)

        all_archives = sorted(os.listdir("versions"))
        [all_archives.pop() for i in range(number)]
        with lcd("versions"):
            [local("rm ./{}".format(a)) for a in archives]

        with cd("/data/web_static/releases"):
            archives = run("ls -tr").split()
            archives = [a for a in archives if "web_static_" in a]
            [archives.pop() for i in range(number)]
            [run("rm -rf ./{}".format(a)) for a in archives]
    
    except getopt.error as err:
        print(str(err))

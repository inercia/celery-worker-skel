#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# XXXX
#
#

from __future__ import with_statement
from __future__ import division

import os
import pprint
import sys

# bootstrap variables
HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = HERE
PYTHON = os.path.abspath(os.path.join(PROJECT_ROOT, 'bin', 'python'))
FABRIC = os.path.abspath(os.path.join(PROJECT_ROOT, 'bin', 'fab'))
FABUTILS_DIR = os.path.join(PROJECT_ROOT, 'buildout')

#  This is our entry point.
if __name__ == '__main__':
    import subprocess

    if not os.path.exists(FABRIC):
        print 'ERROR: fabric not found!'
        print 'ERROR: make sure you have build XXXX before trying to run this script...'
        sys.exit(1)

    if len(sys.argv) > 1:
        #  If we got an argument then invoke fabric with it.
        subprocess.call([FABRIC, '-f', os.path.abspath(__file__)] + sys.argv[1:])
        sys.exit(0)
    else:
        #  Otherwise list our targets.
        subprocess.call([FABRIC, '-f', os.path.abspath(__file__), '--list'])
        print
        print "Run \"%s --help\" for more details" % __file__
        sys.exit(0)


###################################################################################################



from fabric.api                 import run, env, task, parallel, serial, roles, runs_once
from fabric.context_managers    import lcd, cd
from fabric.operations          import put, sudo, local
from fabric.contrib.files       import upload_template
from fabric.decorators          import with_settings

from fabric.colors              import red, green, yellow
from fabric.contrib.console     import confirm
from fabric.operations          import run, sudo
from fabric.context_managers    import cd
from fabric.contrib.files       import sed, upload_template

## load the configuration file
sys.path.append(FABUTILS_DIR)
from fabutils import load_cfg, _exists
load_cfg(env, root = PROJECT_ROOT)


###################################################################################################

@task
def XXXX_build_rpm ():
    """
    Creates the RPM package distribution
    """
    local('make rpm')


@task
@parallel
@roles('integration', 'deployment')
def XXXX_deploy ():
    """
    Deploy the packages in the deployment machines
    """
    print(green("Installing packages at %s" % str(env.host_string)))

    if confirm(red('Install the packages at the %s?' % (env.host_string)), default = False):
        print(yellow("... stopping XXXX"))
        if _exists('/etc/init.d/XXXX'):
            sudo('service XXXX stop')
            sudo('rm -f /etc/init.d/XXXX')

        with cd(env.admin.prefix):
            print(yellow("... cleaning up old RPMs"))
            if not _exists('tmp'): run('mkdir tmp')
            run('rm -rf tmp/*')

        directory = os.path.join(env.admin.prefix, 'tmp')
        with cd(directory):
            print(yellow("... uploading RPMs"))
            for f in env.packages.rpms:
                put(os.path.join(directory, f), '.')

            print(yellow("... installing software"))
            sudo('yum install -R 2 -q -y --nogpgcheck  *.rpm')

            print(red("... XXXX is STOPPED at %s!" % env.host_string))

@task
@parallel
@roles('integration', 'deployment')
def XXXX_start():
    """
    Start the XXXX system
    """
    print(green('Starting XXXX at %s' % (env.host_string)))
    with settings(warn_only = True):
        sudo('rm -f nohup*')
        sudo('[ -f /etc/init.d/XXXX ] && nohup /sbin/service XXXX start || echo "No service script found!!"')

@task
@serial
@roles('integration', 'deployment')
def XXXX_start_i():
    """
    Start the XXXX system (interactive)
    """
    if confirm(red('Start XXXX at %s?' % (env.host_string)), default = False):
        execute(XXXX_start)

@task
@parallel
@roles('integration', 'deployment')
def XXXX_restart():
    """
    Restart the XXXX system
    """
    print(green('Restarting XXXX at %s' % (env.host_string)))
    with settings(warn_only = True):
        sudo('rm -f nohup*')
        sudo('[ -f /etc/init.d/XXXX ] && nohup /sbin/service XXXX restart || echo "No service script found!!"')

@task
@serial
@roles('integration', 'deployment')
def XXXX_restart_i():
    """
    Restart the XXXX system (interactive)
    """
    if confirm(red('Restart XXXX at %s?' % (env.host_string)), default = False):
        execute(XXXX_restart)

@task
@parallel
@roles('integration', 'deployment')
def XXXX_stop():
    """
    Stop the XXXX system
    """
    print(green('Stoping XXXX at %s' % (env.host_string)))
    with settings(warn_only = True):
        sudo('rm -f nohup*')
        sudo('[ -f /etc/init.d/XXXX ] && nohup /sbin/service XXXX stop || echo "No service script found!!"')

@task
@serial
@roles('integration', 'deployment')
def XXXX_stop_i():
    """
    Stop the XXXX system (interactive)
    """
    if confirm(red('Stop XXXX at %s?' % (env.host_string)), default = False):
        execute(XXXX_stop)


@task
@serial
@roles('integration', 'deployment')
def XXXX_update_config():
    """
    Upload the configuration file (after doing replacements)
    """
    dest        = os.path.join(env.admin.prefix, 'conf')
    context     = env.machines[env.host_string]

    if confirm(red('Upload the new configuration files from %s at %s?' %
                   (env.templates.local_dir, env.host_string)),
                default = False):
        for f in env.templates.files:
            print(green('... uploading %s' % (f)))

            sudo('chown -R {user}:{group} {d}'.format(user    = env.admin.user,
                                                      group   = env.admin.group,
                                                      d       = env.admin.prefix))

            upload_template(f, dest,
                            context             = context,
                            use_jinja           = True,
                            template_dir        = env.templates.local_dir,
                            use_sudo            = False,
                            backup              = True)

#
# logs
#

@task
@roles('integration', 'deployment')
def XXXX_tail_log():
    """
    Prints the tail of PREFIX/logs/XXXX.log
    """
    f = os.path.join(env.admin.prefix, 'logs', 'XXXX.log')
    print(green('%s at %s' % (f, env.host_string)))
    with settings(warn_only = True):
        run('[ -f {f} ] && tail {f} || echo "file not found"'.format(f = f))

@task
@parallel
@roles('integration', 'deployment')
def XXXX_cleanup_logs ():
    """
    Cleanup all the logs
    """
    with cd(env.admin.prefix):
        with settings(warn_only = True):
            sudo('[ -d logs ] && rm -rf logs/*')


#
# auxiliary tasks
#

@task
@roles('integration', 'deployment')
def dump_os_env ():
    """
    Dump the OS environment variables on all machines
    """
    with settings(warn_only = True):
        run('export')

@task
@runs_once
def dump_roles ():
    """
    Dumps the current roles list
    """
    roledefs_str = pprint.pformat(env.roledefs, indent = 2)
    print(green("Currently defined roles:\n%s" % roledefs_str))

@task
@runs_once
def dump_env ():
    """
    Dumps the current Fabric environment
    """
    env_str = pprint.pformat(env, indent = 2)
    print(green("Currently defined environment:\n%s" % env_str))

@task
@runs_once
def dump_machines ():
    """
    Dumps the current machines list with their variables
    """
    machines_str = pprint.pformat(env.machines, indent = 2)
    print(green("Currently defined machines:\n%s" % machines_str))



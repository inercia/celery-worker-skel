
import os
import sys

from fabric.utils               import _AttributeDict
from fabric.decorators          import with_settings


try:
    from configparser           import ConfigParser, ExtendedInterpolation
except ImportError:
    print "ERROR: configparser is not installed"
    sys.exit(1)


#: default Fabric configuration file
FABRIC_CFG = 'fabfile.cfg'


###################################################################################################


# some aux functions...
def _exists(path):
    """
    check if a file exists on a remote host

    :param path:
    :return: True if it exists, False otherwise
    """
    with settings(warn_only = True):
        return bool(int(run('[ -e %s ] && echo 1 || echo 0' % path)))



def load_cfg(env, root):
    """
    custom configuration system

    :param env: the environment
    """

    if 'FABRIC_CFG' in os.environ:
        filename = os.environ['FABRIC_CFG']
    else:
        filename = os.path.abspath(os.path.join(root, FABRIC_CFG))
    if not os.path.exists(filename):
        print 'ERROR: Fabric configuration file "%s" not found' % filename
        print 'ERROR: you must use a %s file' % FABRIC_CFG
        print 'ERROR: (or specify the file name on the FABRIC_CFG environment variable)'
        sys.exit(1)

    KEYS_DIR = os.path.abspath(root + '/conf/certs')
    if not os.path.exists(KEYS_DIR):
        print 'ERROR: keys directory "%s" not found' % KEYS_DIR
        sys.exit(1)

    ## load the configuration file
    cfg = ConfigParser(default_section = 'defaults', interpolation = ExtendedInterpolation())
    try:
        with open(filename, 'r') as cfg_file:
            cfg.read_string(unicode(cfg_file.read()))
    except Exception, e:
        print "ERROR: reading %s:" % filename, str(e).lower()
        sys.exit(1)

    # load the roles and machines
    roledefs = {}
    machinedefs = {}
    for section in [x for x in cfg.sections() if x.lower().startswith('role|')]:
        role_name = str(section.lower().replace('role|', '').strip())
        if not role_name in env.roledefs:
            roledefs[role_name] = []

        for host in cfg.options(section):
            machine_section = 'host|' + host
            if cfg.has_section(machine_section):
                machinedefs[str(host)] = {}
                roledefs[str(role_name)].append(str(host.lower()))
                for option in cfg.options(machine_section):
                    machinedefs[host][str(option.upper())] = str(cfg.get(machine_section, option))

    env.roledefs = roledefs
    env.machines = machinedefs

    # ... and the environment sections
    for section in [x for x in cfg.sections() if x.lower().startswith('env|')]:
        env_name = str(section.replace('env|', '').strip())
        if not env_name in env:
            d = {}
            for option in cfg.options(section):
                d[str(option)] = str(cfg.get(section, option))
            env[env_name] = _AttributeDict(d)


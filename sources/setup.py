#!/usr/bin/env python
#


import os

from setuptools import setup, find_packages, Extension


__HERE__    = os.path.abspath(os.path.dirname(__file__))

try:    __VERSION__ = open(os.path.join(__HERE__, '..', 'VERSION'), 'r').read().strip()
except: __VERSION__ = os.environ.get('XXXX_VERSION', '0.1')

try:    __RELEASE__ = open(os.path.join(__HERE__, '..', 'RELEASE'), 'r').read().strip()
except: __RELEASE__ = os.environ.get('XXXX_RELEASE', '1')


setup(
    name                  = 'XXXX',
    version               = '%s-%s' % (__VERSION__, __RELEASE__),
    description           = 'The XXXX software distribution',

    author                = 'unknown',

    maintainer            = 'unknown',
    maintainer_email      = 'unknown@company.com',

    url                   = 'http://www.company.com',
    license               = 'BSD',

    packages              = find_packages(__HERE__),
    package_dir           = {
        '' : '.'
    },

    zip_safe              = False,

    namespace_packages    = ['XXXX'],       # (so we can install other packages under the 'XXXX' namespace)


    entry_points={
        'console_scripts': [
            'XXXX             = XXXX.__main__:main',
            ],

        'celery.commands': [
            'XXXX = XXXX.command:XXXXCommand',
            ],
        },
)




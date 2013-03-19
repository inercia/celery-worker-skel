#!/usr/bin/env python
#


import os

from setuptools import setup, find_packages, Extension


__HERE__ = os.path.abspath(os.path.dirname(__file__))

__APP_NAMESPACE__ = 'XXXX'
__TASKS_NAMESPACE__ = '%s.tasks' % __APP_NAMESPACE__

__TASK_NAME__ = 'basic_task'
__TASK_FULLNAME__ = '%s.%s' % (__TASKS_NAMESPACE__, __TASK_NAME__)


try:    __VERSION__ = open(os.path.join(__HERE__, 'VERSION'), 'r').read().strip()
except: __VERSION__ = os.environ.get('XXXX_VERSION', '0.1')

try:    __RELEASE__ = open(os.path.join(__HERE__, 'RELEASE'), 'r').read().strip()
except: __RELEASE__ = os.environ.get('XXXX_RELEASE', '1')



setup(
    name                  = __TASK_FULLNAME__,
    version               = '%s-%s' % (__VERSION__, __RELEASE__),
    description           = 'A XXXX task',

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

    namespace_packages    = [__APP_NAMESPACE__,
                             __TASKS_NAMESPACE__],

    entry_points = {
        __TASKS_NAMESPACE__: [
            __TASK_NAME__ + ' = ' + __TASK_FULLNAME__,
            ],
        },
)






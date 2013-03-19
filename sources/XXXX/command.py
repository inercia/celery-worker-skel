"""

The :program:`celery XXXX` command

.. program:: celery worker

.. seealso::

    See :ref:`preload-options`.

.. cmdoption:: -t, --test

    A test option.

"""

from __future__ import absolute_import

import os
import sys

import pkg_resources

import logging

from celery.bin.celeryd import WorkerCommand
from celery.bin.base import Option


APP_NAME        = 'XXXX'
TASKS_NAMESPACE = '%s.tasks' % APP_NAME



class XXXXCommand(WorkerCommand):

    doc = __doc__  # parse help from this.

    def run(self, *args, **kwargs):
        plugins = kwargs.get('plugins')
        if plugins and os.path.exists(plugins):
            logging.info('using extra tasks directory "%s"' % plugins)
            pkg_resources.working_set.add_entry(plugins)

        namespace = kwargs.get('namespace')
        logging.info('loading addditional plugins on namespace "%s"' % namespace)
        for entrypoint in pkg_resources.iter_entry_points(group = namespace):
            logging.info('loading entrypoint "%s"' % entrypoint)
            entrypoint.load()

        return super(XXXXCommand, self).run(*args, **kwargs)

    def get_options(self):
        conf = self.app.conf        ## we can access configuration options with conf.VARIABLE
        return (
            Option('', '--plugins',
                   default = None,
                   type = 'string',
                   help = 'directory for looking for additional plugins'),
            Option('', '--namespace',
                   type = 'string',
                   default = TASKS_NAMESPACE,
                   help = 'namespace for the plugins (default: "%s")' % TASKS_NAMESPACE),

        ) + super(XXXXCommand, self).get_options()


def main():
    # Fix for setuptools generated scripts, so that it will
    # work with multiprocessing fork emulation.
    # (see multiprocessing.forking.get_preparation_data())
    if __name__ != '__main__':  # pragma: no cover
        sys.modules['__main__'] = sys.modules[__name__]
    from billiard import freeze_support
    freeze_support()
    worker = WorkerCommand()
    worker.execute_from_commandline()


if __name__ == '__main__':          # pragma: no cover
    main()




Running the software
====================

On development machines
-----------------------

Unit tests
----------


You can run the unit tests with the 'XXXX-tests' script.
For example:

::

    # ./bin/XXXX-tests

After running a test, you can inspect the output in ``nosetests.log``.


Troubleshooting
---------------

* I get this error on the web interface on Mac: ``unknown locale: UTF-8``

  Some version of OS X set a wrong LC_CTYPE or LANG environment variable. Set those environment 
  variables to "C"


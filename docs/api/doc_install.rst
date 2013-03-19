
Installation
============

Build Requirements
------------------

In order to build XXXX, you need:

  * ``Python`` 2.7 or higher (but < 3.x)

  
Development
-----------

For a development build of the software, just do a

::

        make all

This will install all the required components in the local project directory. You only need to do
this once, or if you change the dependencies.


On Linux
--------

Extra repositories for RPM-based systems
----------------------------------------

On CentOS 5.5/RedHat 5.5 you could install some extra repositories:

- the 'Extra Packages for Enterprise Linux (EPEL)' repository for grabbing extra packages.

::

        wget http://download.fedoraproject.org/pub/epel/5/x86_64/epel-release-5-4.noarch.rpm
        sudo rpm -ivh ./epel-release-5-4.noarch.rpm

- the 'rpmforge' repository:

::

        wget http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.2-2.el5.rf.x86_64.rpm
        sudo rpm -ivh ./rpmforge-release-0.5.2-2.el5.rf.x86_64.rpm


RPM creation
------------

If you want to create a RPM, you can do a:

::

        make rpm-clean
        make rpm

This will do a ``distclean`` and then build the broker and node RPMs. You can also create only the broker
or the node RPMs with ``make rpm-broker``  and ``make rpm-node`` respectively.



On Mac OS X
-----------

First, you need the ``XCode development package``. Then you must export these variables before
launching ``make``:

::

        export OSX_VERS=10.7
        export MACOSX_DEPLOYMENT_TARGET=$OSX_VERS
        export OSX_SDK="/Developer/SDKs/MacOSX$OSX_VERS.sdk"
        export ARCHFLAGS="-arch x86_64"
        export LDFLAGS="$ARCHFLAGS -L$OSX_SDK/usr/X11/lib -L$OSX_SDK/usr/lib -L/usr/local/lib -syslibroot,$OSX_SDK"
        export CFLAGS="-O2 $LDFLAGS -I$OSX_SDK/usr/X11/include -I$OSX_SDK/usr/X11/include/freetype2 -I/usr/local/include -isysroot $OSX_SDK"
        export FFLAGS="$ARCHFLAGS"
        export PKG_CONFIG_PATH="/usr/X11/lib/pkgconfig"


You must customize some of these variables:

  * ``OSX_VERS``, depending on the OS X version you are using. If you are using OS X 10.7 (Lion),
  maybe you must use the 10.6 SDK version, depending on the virtualenv version you have... just try.
  * ``arch`` flags, depending on your architecture - ie, ``-arch ppc`` for PowerPC machines

Most of the requirements are already installed with XCode. However, you will need to build from the
source distribution some extra packages:

  * ``swig``
  * ``pcre``
  * ``zeromq``

Make sure these dependencies install their include files and libraries in ``/usr/local/``. Otherwise,
add the corresponding paths to the ``CFLAGS`` and ``LDFLAGS``.


        
Troubleshooting
---------------



* Problems with ``uuid`` in Mac OS X

   If compilation fails with some ``uuid`` related problem, check there is no
   uuid.h in your ``/usr/local/include`` path. If you find the file there, the
   you will have to remove it...

* You are getting this error: ``/usr/include/gnu/stubs.h:7:27: fatal error: gnu/stubs-32.h: No such file or directory``

   You are developing on a 64bits platform but you are compiling for 32bits.
   Install the 32bits development SDK. On Ubuntu you will need:

    ``gcc-*-multilib gcc-multilib lib32gomp1 libc6-dev-i386``

* You are getting a ``png.h`` error on OS X 10.7

   I know. You have to use the 10.6 SDK even on Lion...




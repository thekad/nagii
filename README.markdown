Overview
--------

This is just a simple python library aimed at making it easy for you to create
and generate [nagios](http://www.nagios.org) config files from anywhere.

Nagios objects are modelled in python classes and objects, and you can chain
inheritance in the same way you do in nagios.

This is specially useful if you're generating dynamic configs fairly often,
like if you have a hosts catalog that gets updated on a periodic basis and
you don't want to edit the nagios config each time, you can schedule a job
or cook up a trigger to create the config files for you.

Requirements
------------

The library doesn't really need anything but python's stdlib to work, however
the tests are done with a couple of extra libs for ease of use

How to test
-----------

Once you have a clone of the repo, you should use a virtualenv:

    $ virtualenv --no-site-packages env
    New python executable in env/bin/python
    Installing setuptools............done.
    $

The git ignore file is already set to not care about the right stuff. After
that you have to activate your virtual environment and run the setup script

    $ source env/bin/activate
    (env)$ python setup.py install
    ......................
    ... install output ...
    ......................
    Finished processing dependencies for nagii==0.1
    (env)$

You should be able to run your tests or play with it in your python virtualenv
by now


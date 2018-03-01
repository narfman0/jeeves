jeeves
======

.. image:: https://badge.fury.io/py/jeeves-pa.png
    :target: https://badge.fury.io/py/jeeves-pa

.. image:: https://travis-ci.org/narfman0/jeeves.png?branch=master
    :target: https://travis-ci.org/narfman0/jeeves

Jeeves is a personal assistant similar to alexa/google, based on code from the jasper project.

Installation
------------

To install, we first recommend a python virtual environment. Then::

    pip install jeeves-pa

To populate the initial configuration, run::

    jeeves-populate

Note: default input/output works in most cases, but you will likely have to tweak
this to work for you.

Usage
-----

Run jeeves from the command line with::

    jeeves

TODO
----

* Refactor each plugin to their own pypi package and use entry_points

License
-------

See included LICENSE file for more details

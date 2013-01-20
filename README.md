Gmail applet
============

This is a gmail applet for gnome2. Is under development until check some security faults.

Testing it
----------

>Pre requisites
it's need to be installed python-keyring-gnome and python-keyring

In theory, is enough to put `gmail-checker.server` in `/usr/lib/bonobo/servers` and the rest of the code anywhere you want.

Just change the location in gmail-chercker.server with the path that you put the source.

for debug. run in console `python applet.py -d`

Important.
----------
The applet it's not working. only works with the gui.

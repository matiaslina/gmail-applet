Gmail applet
============

It's a gmail applet for Consort that notify for new mails.

Requisites
----------

*sudo apt-get install python-keyring

*PyNotify2 ~> http://pypi.python.org/pypi/notify2

And I think that thats all.

Install
-------

Run `make install` to install it in the system. If you want to remove it, just do `make uninstall`. Maybe you need to be root to run this commands.

Debug
-----

Just before insert the applet into consort panel, run `python /usr/share/consort-applets/gmail-applet/gmail-factory.py`

Contact
=======

Author: Matias Linares <matiaslina@gmail.com>

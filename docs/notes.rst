Notes
=====

BitTorrent tracker is a pretty basic web application that needs to store and display data.

Some private tracker specific implementations needed:
  * Announce endpoint needs to take a keypass that is unique to the user using the site::

     GET /<keypass>/announce

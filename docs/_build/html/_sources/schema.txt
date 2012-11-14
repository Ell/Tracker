===============
Database Layout
===============

Tracker uses redis to track torrents and user stats

Torrents
--------

Tracker tracks torrent stats in accordance to the bittorrent tracker specification. Every torrent that is tracked must store:

* Number of peers who have the entire file(s) ie. **seeders**
* Number of peers who are still downloading ie. **leeching**
* List of peer addresses with port
* info_hash - the Torrents unique id from the client

Torrent::

    torrent::<info_hash>          # we store torrents in redis based on their info_hash since it will always be unique
    {
      info_hash: <info_hash>,     # the torrents unique info_hash
      user_id: <user_id>,         # user_id of uploader provided by frontend site
      peer_list: [],              # list of peers by user_id
      seeders: {
        user_amount: <amount>,    # amount of users seeding
        users: []                 # list of user_id's currently seeding
      }
      leechers: {
        user_amount: <amount>,    # amount of users leeching
        users: []                 # list of user_id's currently leeching
      }
    }

Torrents should be added via the trackers add torrent endpoint when a torrent is uploaded to the front end site and validated. Front end site should also be responsible for geting the list of files and storing that in its own database.

Users
-----

Users should be initialy added when a user is created on the front end site. The only field that is required to be populated on initial creation is the user_id field, the rest can be set to null. User creation tracker side is handled via the add user api endpoint.

User::

    user::<user_id>                   # users are stored a retrieved based on the `user_id` given by the front end
    {
      user_id: <user_id>,             # user_id given when adding new user
      last_ip: <ipaddress>,           # last known ip of user (optional?)
      last_active: <datetime>,        # timestamp of when user was last active
      active_torrents {               # dict of all torrents user is active in
        seeding: [],                  # list of torrents user is seeding
        leeching: [],                 # list of torrents user is leeching
        torrents: []                  # overall list of all torrents user is active in
      },
      total_upload: <uploadamount>,   # total uploaded
      total_downloaded: <downloaded>, # total downloaded
    }

User ratio isnt calculated by the tracker since thats pretty pointless when we are already tracking total up and down.

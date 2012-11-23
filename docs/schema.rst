===============
Database Layout
===============

Tracker uses RethinkDB to track torrents and user stats

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
      id: <info_hash>,     # the torrents unique info_hash
      peer_list: {
        <peer_id>: {
          ip: <ip>,              # list of peers by user_id
          port: <port>
      }
      seeders: []
      leechers: []
      }
    }

Users
-----

User::

    user::<key>                   # users are stored a retrieved based on the `user_id` given by the front end
    {
      id: <key>,             # user_id given when adding new user
      last_ip: <ipaddress>,           # last known ip of user (optional?)
      last_port: <port>,
      seeding: [],                  # list of torrents user is seeding
      leeching: [],                 # list of torrents user is leeching
      torrents: {
        <info_hash>: {
          uploaded: <>,
          downloaded: <>,
        },
        ..
      }                  # overall list of all torrents user is active in
    },
      total_upload: <uploadamount>,   # total uploaded
      total_downloaded: <downloaded>, # total downloaded
    }

User ratio isnt calculated by the tracker since thats pretty pointless when we are already tracking total up and down.

===============
Database Layout
===============

Tracker uses redis to track torrents and user stats

Torrents
########
Tracker tracks torrent stats in accordance to the bittorrent tracker specification. Every torrent that is tracked must store:
  * Number of peers who have the entire file(s) ie. **seeders**
  * Number of peers who are still downloading ie. **leeching**
  * List of peer addresses with port
  * info_hash - the Torrents unique id from the client

  Torrent::
    .. highlight:: javascript

    torrent:<info_hash> // we store torrents in redis based on their info_hash since it will always be unique
    {
      info_hash: info_hash, // the torrents unique info_hash
      user_id: user_id, // user_id provided by frontend site
      peer_list: [], // list of peers by user_id
      seeders: {
        user_amount: amount, // amount of users seeding
        users: []  // list of user_id's currently seeding
      }
      leechers: {
        user_amount: amount, // amount of users leeching
        users: [] // list of user_id's currently leeching
      }
    }

Users
#####

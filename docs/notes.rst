Notes
=====

BitTorrent tracker is a pretty basic web application that needs to store and display data.

Some private tracker specific implementations needed:
  * Announce endpoint needs to take a keypass that is unique to the user using the site::

     GET /<keypass>/announce

  * When adding a torrent to the tracker we need to track what user added the torrent. This can be done via the trackers api endpoint. Example torrent addition request::

     POST /api
     
     {
      api_key: <key>,
      files: {
        folder: [
          list,
          of,
          files
          sub_folder: [
           test,
           test
          ]
        ]
      },
      user_id: id,
      date_added: date
     }


import json
import os

from flask import Blueprint, render_template, abort, request, g
from lib import bencode

import rethinkdb as r


announce = Blueprint('announce', __name__, template_folder='templates')

@announce.before_request
def before_request():
    conn = r.connect(db_name='tracker')


@announce.teardown_request
def teardown_request(exception):
    conn.close()


@announce.route('/<user_key>/announce')
def announce_request(user_key):
    """TODO:

    * Check if torrent exists
        - check via <info_hash> (this will always be unique)
        - if exists we update said torrent
        - if not exists create new torrent entry
        - add peer to completed list if completed
        - remove if disconnected
        - add peer to leech list if none of the above

    * Update peer in user table
        - get peer using <user_key>
        - add torrent to peers torrent list
        - update peers ip
        - update peers peer_id
        - update peers port
        - update peers total download and upload 
            -- each peer has a list of torrents currently active on
            -- <info_hash>: {upload: <>, download: <>}
            -- check upload and download for torrent compare to given <uploaded> and <left>
            -- use difference to upload peers total upload/download

    """

    data = {
            'info_hash': request.args.get('info_hash', None),
            'peer_id': request.args.get('peer_id', None),
            'port': request.args.get('port', None),
            'uploaded': request.args.get('uploaded', None),
            'downloaded': request.args.get('downloaded', None),
            'left': request.args.get('left', None),
            'compact': request.args.get('compact', None), # 1 - return compact result; 0 - no compact
            'no_peer_id': request.args.get('no_peer_id', None),
            'event': request.args.get('event', None),
            'ip': request.args.get('ip', None), #optional
            'numwant': request.args.get('numwant', 30), #optional
            'key': request.args.get('key', None), #optional for public, needed for private
            'trackerid': request.args.get('trackerid', 'TRACKER'), #optional, no idea what this is for
    }

    for k, v in data.values():
        if k not in ['trackerid', 'event']:
            if not v:
                return bencode.encode({'failure reason': 'missing ' + k})
        else:
            pass

    if data.get('compact', None):
        if data['compact'] == '0':
            return bencode.encode({'failure reason': 'This tracker only supports compact responses'})

    #check if torrent exists
    if not r.table('torrents').get(data['info_hash']):
        #torrent doesnt exist; create it
        #NOTE: do we want to have the frontend create the torrent entries for security purposes? --elgruntox
        r.table('torrents').insert({
            'id': data['info_hash'],
            'peer_list': {},
            'seeders': {
                'users': []
            },
            'leechers': {
                'users': []
            }
        }).run()

    #check if user exists
    if not r.table('users').get(user_key):
        #user doesnt exist; create it
        r.table('users').insert({
            'id': user_key,
            'last_ip': data['ip'],
            'last_port': data['port'],
            'active_torrents': {
                'seeding': [],
                'leeching': [],
                'torrents': {}
            },
            'total_upload': 0,
            'total_downloaded': 0,
        }).run()

    #check if torrent has data specified; if no event just a regular check and we do nothing
    if data['event']:
        if data['event'] == 'started':

            # add torrent to users torrent/leeching list; add peer to torrents peer_list
            user = r.table('users').get(user_key).run()

            # remove user from torrents seeding list if in it
            if data['peer_id'] in user['active_torrents']['seeding']:
                user['active_torrents']['seeding'].remove(data['peer_id'])

            # update users leeching list
            user['active_torrents']['leeching'].append(data['info_hash'])
            user['active_torrents']['leeching'] = list(set(user['active_torrents']['leeching']))

            # update and save user to db
            r.table('users').get(user_key).update(user).run()

            # update torrents leeching list
            torrent = r.table('torrents').get(data['info_hash']).run()
            if data['peer_id'] in torrent['leechers']:
                pass
            else:
                torrent['leechers'].append(data['peer_id'])

            # update torrents peer_list
            torrent['peer_list'][data['peer_id']] = {}
            torrent['peer_list'][data['peer_id']]['ip'] = data['ip']
            torrent['peer_list'][data['peer_id']]['port'] = data['port']

            # save torrent data to db
            r.table('torrents').get(data['info_hash']).update(torrent).run()            


        elif data['event'] == 'stopped':
            # remove torrent from users seeding or leeching list
            user = r.table('users').get(user_key).run()

            # check if in leeching or seeding list; pass if not found
            if data['info_hash'] in user['active_torrents']['seeding']:
                user['active_torrents']['seeding'].remove(data['info_hash'])
            elif data['info_hash'] in user['active_torrents']['leeching']:
                user['active_torrents']['leeching'].remove(data['info_hash'])
            else:
                pass

            # update and save user
            r.table('users').get(user_key).update(user).run()

            # update torrents leeching/seeding/peer list
            torrent = r.table('torrents').get(user_key).run()

            if torrent['peer_list'].get(data['peer_id'], None):
                del torrent['peer_list'][data['peer_id']]
            if data['peer_id'] in torrent['seeders']['users']:
                torrent['seeders']['users'].remove(data['peer_id'])
            if data['peer_id'] in torrent['leechers']['users']:
                torrent['leechers']['users'].remove(data['peer_id'])

            # update and save data to db
            r.table('torrents').get(user_key).update(torrent).run()

        elif data['event'] == 'completed':
            user = r.table('users').get(user_key).run()
            if data['info_hash'] in user['active_torrents']['leeching']:
                user['active_torrents']['leeching'].remove(data['info_hash'])
            user['active_torrents']['seeding'].append(data['info_hash'])
            user['active_torrents']['seeding'] = list(set(user['active_torrents']['seeding']))
            r.table('users').get(user_key).update(user).run()

            torrent = r.table('torrents').get(data['info_hash']).run()
            if data['peer_id'] in torrent['active_torrents']['leeching']:
                torrent['active_torrents']['leeching'].remove(data['info_hash'])
            torrent['active_torrents']['seeding'].append(data['info_hash'])
            r.table('torrents').get(user_key).update(user).run()
        else:
            #malformed request; error out
            return bencode.encode({'failure reason': 'invalid event specified'})

    # update users upload and download stats
    user = r.table('users').get(user_key).run()
    if user['active_torrents']['torrents'].get(data['info_hash'], None):
        uploaded = int(data['uploaded']) - user['active_torrents']['torrents'].get(data['info_hash'], 0)
        downloaded = int(data['downloaded']) - user['active_torrents']['torrents'].get(data['info_hash'], 0)
        user['active_torrents']['torrents'][data['info_hash']]['uploaded'] = user['active_torrents']['torrents'][data['info_hash']]['uploaded'] + uploaded
        user['active_torrents']['torrents'][data['info_hash']]['downloaded'] = user['active_torrents']['torrents'][data['info_hash']]['downloaded'] + downloaded
        user['total_upload'] = user['total_upload'] + uploaded
        user['total_downloaded'] = user['total_downloaded'] + downloaded
    else:
        user['active_torrents']['torrents'][data['info_hash']]['uploaded'] = int(data['uploaded'])
        user['active_torrents']['torrents'][data['info_hash']]['downloaded'] = int(data['downloaded'])
        user['total_upload'] = user['total_uploaded'] + int(data['uploaded'])
        user['total_downloaded'] = user['total_downloaded'] + int(data['downloaded'])

    r.table('users').get('user_key').update(user).run()

    # generate response
    torrent = r.table('torrents').get(data['info_hash']).run()

    peer_list = []
    for peerid, values in torrent['peer_list'].iteritems():
        peer = (peerid, torrent['peer_list'][peerid]['ip'], torrent['peer_list'][peerid]['port'])
        peer_list.append(peer)

    resp = {}
    resp['interval'] = 900
    resp['min interval'] = 900
    resp['trackerid'] = data['trackerid']
    resp['complete'] = len(torrent['seeders']['users'])
    resp['incomplete'] = len(torrent['leechers']['users'])
    resp['peers'] = bencode.make_peer_list(peer_list)

    return bencode.encode(resp)


@announce.route('/<user_key>/scrape')
def announce_scrape(user_key):
    pass

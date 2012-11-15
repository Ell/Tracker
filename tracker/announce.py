import json
import os

from flask import Blueprint, render_template, abort, request
from lib import bencode
import redis


r = redis.Redis()
announce = Blueprint('announce', __name__, template_folder='templates')

@announce.route('/<user_key>/announce')
def announce_request(user_key):
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
        if k not in ['trackerid']:
            if not v:
                return bencode.encode({'failure reason': 'missing ' + k})
        else:
            pass

    if data.get('compact', None):
        if data['compact'] == '0':
            return bencode.encode({'failure reason': 'This tracker only supports compact responses'})

    if data['event'] == 'started':
        # add peer to torrents leeching list
        pass

    if data['event'] == 'stopped':
        # remove peer from torrent
        pass

    if data['event'] == 'completed':
        # add peer to torrents seeding list
        pass

    torrent = r.hgetall('torrent:' + data['info_hash'])

    resp = {}
    resp['interval'] = '600'
    resp['tracker id'] = data['trackerid']
    resp['complete'] = torrent['seeders']['user_amount']
    resp['incomplete'] = torrent['seeders']['user_amount']

    peers = json.loads(torrent['peers'])
    peerList = []

    for k, v in peers.iteritems():
        p = (k, v['ip'], v['port'])
        peerList.append(p)

    resp['peers'] = bencode.make_compact_peer_list(peerList[:numwant])

    return bencode.encode(resp)


@announce.route('/<user_key>/scrape')
def announce_scrape(user_key):
    pass

from flask import Blueprint, render_template, abort, request


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
            'numwant': request.args.get('numwant', None), #optional
            'key': request.args.get('key', None), #optional for public, needed for private
            'trackerid': request.args.get('trackerid', None), #optional, no idea what this is for
    }

    for k, v in data.values():
        if k not in ['compact', 'ip', 'numwant', 'trackerid']:
            if not v:
                return 404
        else:
            pass



    return "Hey"

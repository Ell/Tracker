from flask import Blueprint, render_template, abort, request


api = Blueprint('api', __name__, template_folder='templates')

@api.route('/torrent/<torrentID>', methods=['GET'])
def get_torrent(torrentID):

    """
    .. py:function get_torrent(torrentID)

    Returns a torrent with the id of `torrentID` and returns a JSON representation of it.
    See `Database` in documentation for example output

    """

    return torrentID


@api.route('/torrent', methods=['POST'])
def add_torrent():

    """
    .. py:function add_torrent()
    
    Creates a new torrent and returns its id.

    **POST Parameters**
    :param info_hash: torrents unique info_hash; this is also the torrents id
    :param user_id: user id of the user who uploaded the torrent
    """

    return 'add_torrent'


@api.route('/torrent/<torrentID>', methods=['PUT'])
def update_torrent(torrentID):
    """
    .. py:function update_torrent(torrentID)

    Updates a torrent with the id of torrentID. All parameters are optional during an update. Expects JSON in the PUT request

    param: info_hash: the torrents info_hash (aka the torrentID)
    param: user_id: user id of the uploader
    param: peer_list: list of all peers currently using torrent

    param: seeders: dictionary containing information on seeders currently seeding the torrent
    param: user_amount: list in seeders; number of current seeders on torrent
    param: users: list of user_id's currently seeding; in seeders

    param: leechers: dictionary containing information on users currently leeching torrent
    param: user_amount: list in leechers; current amount of leechers on torrent
    param: users: list of user_id's currently leeching; in leechers

    For JSON formating example please refer to `Database` documentation
    """

    return torrentID


@api.route('/user', methods=['POST'])
def add_user():
    """
    .. py:function add_user()

    Creates a new user. All parameters are POST parameters

    param: user_id: user_id for user. should match with frontends user id 1:1.
    """

    return 'add_user'


@api.route('/user/<userID>', methods=['GET'])
def get_user(userID):
    """
    .. py:function get_user(userID)

    Gets user with the user_id of `userID`

    param: userID: user_id of user
    """

    return userID


@api.route('/user/<userID>', methods=['PUT'])
def update_user(userID):
    """
    .. py:function update_user(userID)

    Updates user with the user_id of `userID`. Expects JSON. Parameters are PUT params.

    **Example parameters can be found in the `Database` section of the documentation**
    """

    return userID

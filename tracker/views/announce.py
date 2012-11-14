from flask import Blueprint, render_template, abort, request


announce = Blueprint('announce', __name__, template_folder='templates')

@announce('/<user_key>/announce')
def announce(user_key):
    pass

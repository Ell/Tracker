from flask import Blueprint, render_template, abort, request


api = Blueprint('api', __name__, template_folder='templates')

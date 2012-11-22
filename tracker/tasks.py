from __future__ import absolute_import
import json

from tracker.celery import celery
import redis

r = redis.Redis()


@celery.task
def add_peer(user_id, info_hash, secret_key):
	if r.hexists('torrent:'+info_hash, 'peers'):
		peers = json.loads(r.hget('torrent:'+info_hash, peers))
	else:
		peers = {}

	if r.hexists('torrent:'+info_hash, 'seeders')


@celery.task
def add_seeder(user_id, info_hash, secret_key):
	pass


@celery.task
def remove_peer(user_id, info_hash, secret_key):
	pass
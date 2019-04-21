import json
import time

from flask import Flask, request, jsonify, send_file, abort

import data

app = Flask(__name__)

SESSION_ID = "366F9408E33F7715ADFBAF812510B662"
user_session_id = None
email = "test@wp.pl"
password = "pass"

def is_authorized():
	global user_session_id
	return user_session_id is not None

@app.errorhandler(401)
def unauthorized(error):
	response = jsonify({'code': 401, 'message': error.description})
	response.status_code = 401
	return response

@app.errorhandler(404)
def not_found(error):
	response = jsonify({'code': 404, 'message': error.description})
	response.status_code = 404
	return response

# ----------------------------------------------------------------------------------------------------------------------
# UsersAPI
@app.route("/api/users/register", methods=['POST'])
def register_user():
	global user_session_id
	global email
	global password

	request_body = request.get_json()
	email = request_body['email']
	password = request_body['password']
	user_session_id = SESSION_ID

	response = app.response_class(
		response=user_session_id,
		status=200,
		mimetype='application/json'
	)
	return response

@app.route("/api/users/login", methods=['POST'])
def login_user():
	global user_session_id
	global email
	global password

	request_body = request.get_json()
	if email != request_body['email'] or password != request_body['password']:
		abort(401, 'Invalid email or password')

	user_session_id = SESSION_ID
	response = app.response_class(
		response=user_session_id,
		status=200,
		mimetype='application/json'
	)
	return response

@app.route("/api/users/logout", methods=['POST'])
def logout_user():
	global user_session_id
	user_session_id = None
	response = app.response_class(
		status=200
	)
	return response

# ----------------------------------------------------------------------------------------------------------------------
# PocketsAPI
@app.route("/api/pockets", methods=['POST'])
def save_pocket():
	if is_authorized() is False:
		abort(401, 'You are not authorized to access')

	request_body = request.get_json()

	json_dict = {}
	json_dict['id'] = get_available_id(data.storage)
	json_dict['title'] = request_body['title']
	json_dict['description'] = request_body['description']
	json_dict['source'] = request_body['source']
	json_dict['tags'] = request_body['tags']
	json_dict['link'] = request_body['link']
	json_dict['createdDate'] = int(time.time())

	data.storage.append(json_dict)

	response = app.response_class(
		response=json.dumps(json_dict),
		status=201,
		mimetype='application/json'
	)
	return response

@app.route("/api/pockets", methods=['GET'])
def find_pockets():
	if is_authorized() is False:
		abort(401, 'You are not authorized to access')

	tag_name = request.args.get('tag')

	if tag_name is None:
		bookmark_list = data.storage
	else:
		bookmark_list = [bookmark for bookmark in data.storage if tag_name in bookmark['tags']]
	response = app.response_class(
		response=json.dumps(bookmark_list),
		status=200,
		mimetype='application/json'
	)
	return response

@app.route("/api/pockets/<id>", methods=['GET'])
def find_pocket_blob_by_id(id):
	if is_authorized() is False:
		abort(401, 'You are not authorized to access')

	bookmark_exist = False
	for item in data.storage:
		if item['id'] == int(id):
			bookmark_exist = True
			data.storage.remove(item)
			break

	if bookmark_exist is False:
		abort(404, 'Resource with id = %s not found'.format(id))
	else:
		return send_file("prtscr.jpeg", mimetype='image/jpeg')

@app.route("/api/pockets/<id>", methods=['DELETE'])
def delete_pocket_by_id(id):
	if is_authorized() is False:
		abort(401, 'You are not authorized to access')

	bookmark_exist = False
	for item in data.storage:
		if item['id'] == int(id):
			bookmark_exist = True
			data.storage.remove(item)
			break

	if bookmark_exist is False:
		abort(404)
	else:
		return app.response_class(
			status=204,
			mimetype='application/json'
		)


# ----------------------------------------------------------------------------------------------------------------------
# TagsAPI
@app.route("/api/tags")
def find_all_tags():
	if is_authorized() is False:
		abort(401, 'You are not authorized to access')

	tags_list = [bookmark['tags'] for bookmark in data.storage]
	tags_set = set(tags_list)
	response = app.response_class(
		response=json.dumps(tags_set),
		status=200,
		mimetype='application/json'
	)
	return response


def update_tags(tags_from_request):
	for tag in tags_from_request:
		existing = False
		for i in range(len(data.tag)):
			if tag in data.tag[i].values():
				data.tag[i]["tag_size"] += 1
				existing = True
				continue
		if not existing:
			new_tag = {'_id': get_available_id(data.tag), 'name': tag, 'tag_size': 1}
			data.tag.append(new_tag)


def get_available_id(list):
	return list[-1]['id'] + 1


if __name__ == '__main__':
	app.run(port=8013, debug=True)

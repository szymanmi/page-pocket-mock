import json
import time

from flask import Flask, request, jsonify

import data

app = Flask(__name__)


@app.route("/api/test")
def hello():
	return "Hello World!"


# example: http://127.0.0.1:8013/api/tags/name/info
@app.route("/api/tags/name/<name>")
def getbytag(name):
	new_list = []
	requested_tag = name
	for item in data.storage:
		if requested_tag in item["tags"]:
			new_list.append(item)

	new_list = json.dumps(new_list)
	return new_list


@app.route("/api/tags")
def getalltag():
	return json.dumps(data.tag)


@app.route("/api/pockets", methods=['GET'])
def getallwebpages():
	return json.dumps(data.storage)


@app.route("/api/pockets", methods=['POST'])
def addpage():
	request_data = request.get_json()

	json_dict = {}
	json_dict['_id'] = get_available_id(data.storage)
	json_dict['description'] = request_data['description']
	json_dict['source'] = request_data['source']
	json_dict['tags'] = request_data['tags']
	json_dict['link'] = request_data['link']
	json_dict['createdDate'] = int(time.time())

	data.storage.append(json_dict)
	update_tags(request_data['tags'])

	print(data.tag)
	resp = jsonify(success=True)
	resp.status_code = 201
	return resp


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
	return list[-1]['_id'] + 1


if __name__ == '__main__':
	app.run(port=8013, debug=True)

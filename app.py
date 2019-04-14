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
	json_dict['_id'] = get_available_id()
	json_dict['description'] = request_data['description']
	json_dict['source'] = request_data['source']
	json_dict['tags'] = request_data['tags']
	json_dict['link'] = request_data['link']
	json_dict['createdDate'] = int(time.time())

	data.storage.append(json_dict)

	print(data.storage)
	resp = jsonify(success=True)
	resp.status_code = 201
	return resp


def get_available_id():
	return data.storage[-1]['_id'] + 1


if __name__ == '__main__':
	app.run(port=8013, debug=True)

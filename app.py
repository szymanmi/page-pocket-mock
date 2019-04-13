from flask import Flask, request, jsonify
from datetime import datetime
import json
import data

app = Flask(__name__)


@app.route("/api/test")
def hello():
	return "Hello World!"


# example: http://127.0.0.1:8013/api/getbytag?tag=info
@app.route("/api/getbytag")
def getbytag():
	new_list = []
	requested_tag = request.args.get('tag')
	for item in data.storage:
		if requested_tag in item["tags"]:
			new_list.append(item)

	new_list = json.dumps(new_list)
	return new_list


@app.route("/api/getalltag")
def getalltag():
	return json.dumps(data.tag)


@app.route("/api/pockets")
def getallwebpages():
	return json.dumps(data.storage)


@app.route("/api/addpage", methods=['POST'])
def addpage():
    request_data = request.get_json()

    json_dict = {}
    json_dict['_id'] = request_data['_id']
    json_dict['description'] = request_data['description']
    json_dict['source'] = request_data['source']
    json_dict['tags'] = request_data['tags']
    json_dict['link'] = request_data['link']
    json_dict['createdDate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    data.storage.append(json_dict)
    
    resp = jsonify(success=True)
    resp.status_code = 201
    return resp


if __name__ == '__main__':
	app.run(port=8013, debug=True)

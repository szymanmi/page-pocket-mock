from flask import Flask, request, jsonify
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


if __name__ == '__main__':
	app.run(port=8013)

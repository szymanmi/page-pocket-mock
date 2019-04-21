# page-pocket-mock

## Getting started

Project requires python 3.7.3

# Setting up

1. Clone the repository:

```$ git clone https://github.com/szymanmi/page-pocket-mock.git```

2. Enter the project directory:

```$ cd page-pocket-mock```

3. Create virtual env:

```$ python3 -m venv env```

4. Activate the env:

```$ source env/bin/activate```

5. Install dependecies:

```$ pip install -r requirements.txt```

# Running the app

```$ python3 app.py```

To test go to  ```http://127.0.0.1:8013/api/test```, you should get ```Hello world``` message.

To test if the page was added:

```
$ curl -X POST \
  http://127.0.0.1:8013/api/pockets \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 3b32f3ef-f77d-4098-8b82-5f0cd0372180' \
  -H 'cache-control: no-cache' \
  -d '{
	 "description": "desc4",
	 "source": "www.reddit.com",
	 "tags": ["info", "fun"],
	 "link": "https://www.reddit.com"
}'
```

# Finish
When you have finished working with the app, deactivate the virtual environment:

```$ deactivate```

## Requests
|                         | GET                                                                                                                                                       | POST                                                                                                      |
|-------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| `/api/pockets`          | [ {"id": 531, "description": "desc1", "source": "www.interia.pl", "tags": ["info"], "link": "https://www.interia.pl", "createdDate": "1555234406"} ... ] | {"description": "desc10", "source": "www.reddit.com", "tags": ["info"], "link": "https://www.reddit.com" } |
| `/api/pockets/<id>`      | prtscr.jpeg                                                                                                                                               | -                                                                                                         |
| `/api/tags`             | [ {"id": 123, "name": "info", "tag_size": 2} ... ]                                                                                                       | -                                                                                                         |
| `/api/tags/name/<name>` | [ {"id": 531, "description": "desc1", "source": "www.interia.pl", "tags": ["info"], "link": "https://www.interia.pl", "createdDate": "1555234406"} ... ] | -                                                                                                         |

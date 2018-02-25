install:
	pip install -r requirements.txt

run:
	FLASK_APP=page.py FLASK_DEBUG=1 flask run

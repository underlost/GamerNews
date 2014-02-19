web:      newrelic-admin run-program gunicorn gamernews.wsgi -b 0.0.0.0:\$PORT -w 3 -k gevent --max-requests 250
worker:   python manage.py celeryd -E -B --loglevel=INFO
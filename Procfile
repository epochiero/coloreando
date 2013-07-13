web: gunicorn -b 0.0.0.0:8000 --worker-class socketio.sgunicorn.GeventSocketIOWorker --settings=coloreando.settings.prod coloreando.wsgi:application
redis: redis-server

web: gunicorn -b 0.0.0.0:8000 --log-level debug --worker-class socketio.sgunicorn.GeventSocketIOWorker --settings coloreando.settings.prod -p /tmp/gunicorn.pid coloreando.wsgi:application 
redis: redis-server

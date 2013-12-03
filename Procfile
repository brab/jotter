#web: sh -c 'cd ./server/ && exec gunicorn server.wsgi'
#web: sh -c 'cd ./server/ && exec python3.3 manage.py runserver 0.0.0.0:$PORT'
#web: python 3.3 server/manage.py runserver 0.0.0.0:$PORT
#web: python3.3 server/manage.py run_gunicorn -b 0.0.0.0:$PORT
web: gunicorn -b 0.0.0.0:$PORT server.server.wsgi:application

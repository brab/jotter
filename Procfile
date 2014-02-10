#web: python3.3 server/manage.py runserver 0.0.0.0:$PORT
#web: sh -c 'cd ./server/ && exec python3.3 manage.py runserver 0.0.0.0:$PORT'
web: python3.3 server/manage.py run_gunicorn -b "0.0.0.0:$PORT"

export FLASK_APP=run.py

export TRAIN_MODEL=FALSE
flask db upgrade

export TRAIN_MODEL=TRUE
uwsgi uwsgi.ini

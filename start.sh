export FLASK_APP=run.py

export TRAIN_MODEL=FALSE
flask db upgrade

export TRAIN_MODEL=TRUE
uwsgi -H /Users/simonlindgren/.python-envs/mimir-sf uwsgi.ini

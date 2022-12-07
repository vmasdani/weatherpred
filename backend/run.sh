python3 -m venv ./venv &&\
./venv/bin/python3 -m pip install --upgrade pip &&\
./venv/bin/python3 -m pip install -r requirements.txt &&\
./venv/bin/python3 -m alembic upgrade head &&\
./venv/bin/python3 app.py 
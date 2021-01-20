release: ./clean-db && ./migrate-db.sh
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker forsguiden.main:app
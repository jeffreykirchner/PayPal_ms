echo "*** Startup.sh ***"
echo "Run Migrations:"
python manage.py migrate
echo "Start gunicorn:"
gunicorn --bind=0.0.0.0 --timeout 30 --max-requests 500 --max-requests-jitter 10  _esi_PayPal_ms.wsgi

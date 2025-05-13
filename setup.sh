echo "Setup ESI Paypal MS"
sudo service postgresql restart
sudo service redis-server start
echo "Drop paypal db: enter db password"
dropdb paypal -U dbadmin -h localhost -i -p 5432
echo "Create database: enter db password"
createdb -h localhost -p 5432 -U dbadmin -O dbadmin paypal
echo "Restore database? (y/n)"
read restore
if [ "$restore" = "y" ]; then
    echo "Restore database: enter db password"
    pg_restore -v --no-owner --role=dbowner --host=localhost --port=5432 --username=dbadmin --dbname=paypal database_dumps/chapman_experiments_ppms.sql
else
    python manage.py migrate
    echo "Create Super User:"
    python manage.py setup_superuser_with_profile
    python manage.py setup_site_parameters
fi
echo "Setup complete."
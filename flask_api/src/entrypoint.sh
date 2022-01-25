# Create the Database and tables.
echo "Apply database migrations"; python manage.py create_db;
# Run the Flask App.
echo "Run Flask App"; python manage.py run -h 0.0.0.0;
# Computers-Shop

Online store of computer accessories.

The data is parsed from the DNS site. The parsing code is located in my DNS-parser repository.

* After cloning the repository, enter personal parameters in the .env.prod and .env.prod.db files

* It is necessary to grant write permissions for the root and its incoming files and folders (* chmod -R 755 (your path to the root folder) )

Starting the project build:

* docker-compose up -d --build

After successfully running the project in Docker, write the following commands in the console to perform migrations and collect static files:

* docker-compose exec web python manage.py collectstatic
* docker exec $(docker ps -f name=(YOUR DIRECTORY NAME)_db_1 -q) pg_restore -U postgres -d (YOUR POSTGRESQL DATABASE) /re_store_db

The application will be available at: http://localhost:1337

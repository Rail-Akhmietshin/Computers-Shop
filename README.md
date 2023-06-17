# Online store of computers and their components

## P.S.

The data is parsed from the DNS-shop site. The parsing code is located in my DNS-parser repository.

## Description

The site is fully adaptive for all types of devices.

The site supports the following features:

* The header is equipped with all categories of goods in the form of a drop-down list, a search engine for all goods, the possibility of authorization, a basket with selected goods for purchase

* Authorization is equipped with the ability to log in through third-party social networks or enter your own email and password, where you will receive an email to confirm your account. 

* The main page, which contains an illustration in the form of a carousel with the latest news in the computer field, the main categories of components and the opportunity to assemble your own computer with the help of specialists

* The list and its pagination, filtering and sorting, primary and detailed characteristics of each product, the ability to add an item to the cart

* The shopping cart is equipped with the ability to select the quantity of goods to purchase and place an order

## Deployment with Docker

* After cloning the repository, enter personal parameters in the .env.prod and .env.prod.db files

* It is necessary to grant write permissions for the root and its incoming files and folders (* chmod -R 755 (your path to the root folder) )

Starting the project build:

* docker-compose up -d --build

After successfully running the project in Docker, write the following commands in the console to perform migrations and collect static files:

* docker-compose exec web python manage.py collectstatic
* docker exec $(docker ps -f name=(YOUR DIRECTORY NAME)_db_1 -q) pg_restore -U postgres -d (YOUR POSTGRESQL DATABASE) /re_store_db

The application will be available at: http://localhost:1337

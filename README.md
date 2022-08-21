# dimatech

## About

Test assignment for DimaTech Ltd

## Installation and using

This project provides you a working Django environment without requiring you to install Python/Django, a web server, and any other server software on your local machine. For this, it requires Docker and Docker Compose.

1. Install [Docker](https://docs.docker.com/engine/installation/) and [Docker-compose](https://docs.docker.com/compose/install/);

2. Clone this project and then cd to the project folder;

3. Create your own .env file by copying .env.example:
    ```sh
    $ cp src/.env.example src/.env
    ```

4. Update the environment variables in the docker-compose.yml and .env files.

5. Build the images and run the containers:
     ```sh
    $ docker-compose -f docker-compose.yml up -d --build
    ```

6. You've done! Main page is available on http://localhost

7. After finishing work, you can stop running containers:
    ```sh
    $ docker-compose down
    ```

## Site with ssl certificate

To use it, you must have a server and a domain configured

1. Create a nginx configuration file to handle ssl:
    ```sh
    $ mkdir conf.d
    $ cp ./Docker/nginx/nginx.prod.conf ./conf.d/nginx.conf
    ```

2. Update the environment variables:

    2.1.  In the docker-compose.prod.yml variable "CERTBOT_EMAIL"

    2.2. In the conf.d/nginx.conf variable "server_name"
    
    2.3 In the src/.env add variable "CSRF_TRUSTED_ORIGINS=https://your_web_site"

3. Build the images and run the containers:
     ```sh
    $ docker-compose -f docker-compose.prod.yml up -d --build
    ```

4. You've done! Main page is available on https://your_web_site

## Testing

To use the site, you have access to the main addresses:

*/* - home page

*/product/* - for viewing and editing products

   ```
   Required request fields for POST method
   title: text
   description: text
   price: float
   ```

*/customer-bill/* - to view and edit customer bills

   ```
   Required request fields for POST method
   bill_balance: float
   ```

*/transaction/* - to view and edit transactions

   ```
   Required request fields for POST method
   user_id: int
   bill_id: int
   amount: float
   ```

*/purchase/* - to view and edit purchases

   ```
   Required request fields for POST method
   product_id: int
   bill_id: int
   ```

GET */auth/users/* - for viewing users

POST */auth/users/* - for creating users

   ```
   Required request fields for POST method
   username: text
   password: text
   ```

GET */auth/users/activate/{uid}/{token}/* - for activating users

POST */auth/jwt/create/* - to create a jwt token

   ```
   Required request fields for POST method
   username: text
   password: text
   ```

POST */payment/webhook* - for sending webhook of transactions

   ```
   Required request fields for POST method
   signature: text
   transaction_id: int
   user_id: int
   bill_id: int
   amount: float
   ```

PATCH */auth/users/{id}/* - for editing users
   ```
   Request fields
   password: text
   email: int
   is_active: bool - to enable/disable the user
   ```

*/admin/* - admin panel for interaction with the database tables

**Note**: default users can view accounts, transactions and purchases associated with them. Administrators can view the data of all users

To create an administrator account run the command
   ```sh
    $ docker-compose run django python manage.py createsuperuser
   ```

You can then grant administrator rights through the admin panel

## License

This project is licensed under the [MIT license](LICENSE).

#docker-compose.yml trebuie sa fie in director

touch Dockerfile_mysql
echo "from mysql:8">Dockerfile_mysql
echo "EXPOSE 3306">>Dockerfile_mysql
docker build -t mysql_image:v1 -f Dockerfile_mysql .

touch Dockerfile_php
echo "FROM php:8.0-apache">Dockerfile_php
echo "EXPOSE 80">>Dockerfile_php
docker build -t php_image:v1 -f Dockerfile_php .

touch Dockerfile_phpmyadmin
echo "FROM phpmyadmin">Dockerfile_phpmyadmin
echo "EXPOSE 80">>Dockerfile_phpmyadmin
docker build -t phpmyadmin_image:v1 -f Dockerfile_phpmyadmin .

docker-compose up -d

sudo chmod -R a+rwx apps/
touch apps/php1/src/index.php
echo '!-- ./php/index.php -->
<html>
<head>
 <title>Hello World</title>
 </head>
 <body>
 <?php
 echo "Hello, World!";
 ?>
 </body>
</html>'>apps/php1/src/index.php

cp apps/php1/src/index.php apps/php2/src/index.php
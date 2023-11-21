mkdir Proiect_docker_normal
cd Proiect_docker_normal/

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

docker run -d -p 3306:3306 --name my-database -e MYSQL_ROOT_PASSWORD=root -e MYSQL_PASSWORD=root -e MYSQL_USER=user -e MYSQL_DATABASE=mydb -v ./apps/mysql:/var/lib/mysql mysql_image:v1

docker run -d -p 8080:80 -v ./apps/php1/src:/var/www/html/ --name php-apache1 php_image:v1

docker run -d -p 8081:80 -v ./apps/php2/src:/var/www/html/ --name php-apache2 php_image:v1

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

docker run -d -p 8082:80 --name phpmyadmin -e PMA_HOST=mydb -e PMA_PORT=3306 -e PMA_ARBITRARY=1 --restart always phpmyadmin_image:v1

#We can now connect to phpmyadmin on localhost:8082 with server 172.16.0.2, user user, password root
#We can now navigate to index.php via localhost:8080 or